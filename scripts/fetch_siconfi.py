#!/usr/bin/env python3
"""
fetch_siconfi.py — Atualiza snapshots RREO do Siconfi em data/{uf}.json

Uso:
  python scripts/fetch_siconfi.py            # todos os 6 estados
  python scripts/fetch_siconfi.py sp         # só SP
  python scripts/fetch_siconfi.py sp mg rj   # SP, MG e RJ

Adicionado automaticamente em 2026-06-26. Atualizado mensalmente via
.github/workflows/update-siconfi.yml.

Fonte: https://apidatalake.tesouro.gov.br/docs/siconfi/
"""

import json
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

UFS = {
    "sp": 35,
    "mg": 31,
    "rj": 33,
    "ba": 29,
    "pr": 41,
    "rs": 43,
}

EXERCICIO = 2023  # último ano com P6 fechado; ajuste quando virar 2024 P6
PERIODO = 6       # 6º bimestre = dados consolidados do ano
TIMEOUT = 60      # segundos


def find(items, cod_conta, coluna):
    for i in items:
        if i.get("cod_conta") == cod_conta and i.get("coluna") == coluna:
            return i
    return None


def val(x):
    return x["valor"] if x else None


def fetch_estado(uf, code):
    url = (
        f"https://apidatalake.tesouro.gov.br/ords/siconfi/tt/rreo"
        f"?an_exercicio={EXERCICIO}&nr_periodo={PERIODO}"
        f"&co_tipo_demonstrativo=RREO&id_ente={code}"
    )
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        data = json.loads(resp.read().decode("utf-8"))

    items = data["items"]
    if not items:
        raise RuntimeError(f"Siconfi retornou vazio para {uf}")

    recv_prev = find(items, "ReceitasExcetoIntraOrcamentarias", "PREVISÃO INICIAL")
    recv_atu = find(items, "ReceitasExcetoIntraOrcamentarias", "PREVISÃO ATUALIZADA (a)")
    recv_real = find(items, "ReceitasExcetoIntraOrcamentarias", "Até o Bimestre (c)")
    desp_di = find(items, "DespesasExcetoIntraOrcamentarias", "DOTAÇÃO INICIAL (d)")
    desp_da = find(items, "DespesasExcetoIntraOrcamentarias", "DOTAÇÃO ATUALIZADA (e)")
    desp_emp = find(items, "DespesasExcetoIntraOrcamentarias", "DESPESAS EMPENHADAS ATÉ O BIMESTRE (f)")
    desp_liq = find(items, "DespesasExcetoIntraOrcamentarias", "DESPESAS LIQUIDADAS ATÉ O BIMESTRE (h)")
    desp_pag = find(items, "DespesasExcetoIntraOrcamentarias", "DESPESAS PAGAS ATÉ O BIMESTRE (j)")

    return {
        "uf": uf.upper(),
        "nome": items[0].get("instituicao"),
        "codigoIbge": code,
        "fonte": "Siconfi - Tesouro Nacional",
        "demonstrativo": "RREO",
        "exercicio": EXERCICIO,
        "periodo": PERIODO,
        "periodicidade": "Bimestral",
        "dataColeta": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        "urlOriginal": url,
        "populacao": items[0].get("populacao"),
        "receitaPrevisaoInicial": val(recv_prev),
        "receitaPrevisaoAtualizada": val(recv_atu),
        "receitaRealizada": val(recv_real),
        "despesaDotacaoInicial": val(desp_di),
        "despesaDotacaoAtualizada": val(desp_da),
        "despesaEmpenhada": val(desp_emp),
        "despesaLiquidada": val(desp_liq),
        "despesaPaga": val(desp_pag),
    }


def main():
    args = [a.lower() for a in sys.argv[1:]]
    targets = {k: v for k, v in UFS.items() if not args or k in args}

    repo_root = Path(__file__).resolve().parent.parent
    data_dir = repo_root / "data"
    data_dir.mkdir(exist_ok=True)

    falhas = []
    for uf, code in targets.items():
        try:
            payload = fetch_estado(uf, code)
            out = data_dir / f"{uf}.json"
            out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
            rec = payload["receitaRealizada"]
            desp = payload["despesaEmpenhada"]
            print(f"OK  {uf.upper()} rec={rec:>20,.0f}  desp={desp:>20,.0f}")
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, RuntimeError) as e:
            print(f"ERR {uf.upper()} {e}")
            falhas.append((uf, str(e)))

    if falhas:
        sys.exit(f"\n{len(falhas)} estado(s) falharam: {falhas}")


if __name__ == "__main__":
    main()
