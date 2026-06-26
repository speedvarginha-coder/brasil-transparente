# Brasil Transparente — AGENTS.md

Documentação de setup e arquitetura para agentes IA trabalharem neste projeto.

## Repositório

- **GitHub:** https://github.com/speedvarginha-coder/brasil-transparente
- **Branch:** `main`
- **Visibilidade:** público
- **Workspace local:** `C:\Users\Desktop\Desktop\Brasil Transparente`

## Arquitetura

**Stack:** HTML estático + CSS + JS vanilla + JSON cacheado + GitHub Actions.
**Sem build step, sem framework, sem dependência externa em runtime.**

```
HTML canônico ──► fetch raw.githubusercontent.com ──► JSONs em data/{uf}.json
                                                       ▲
GitHub Action (cron mensal) ──► scripts/fetch_siconfi.py ──► Siconfi API
```

### Por que JSON cacheado (não Cloudflare Worker, não backend)

- CORS do Tesouro Nacional bloqueia fetch direto do browser
- JSON commitado no repo tem CORS liberado via `raw.githubusercontent.com`
- Histórico de mudanças de dados fica no `git log` (auditável)
- Funciona offline
- Zero custo (GitHub Actions free 2.000 min/mês, gasto ~3 min/mês)
- Cidadão pode ver exatamente qual versão dos dados viu em qualquer captura

## Estrutura de pastas

```
.github/workflows/update-siconfi.yml   # Action mensal + on:push
scripts/fetch_siconfi.py              # Script server-side (sem CORS)
data/{sp,mg,rj,ba,pr,rs}.json         # Snapshots RREO 2023 P6 do Siconfi
data/_raw_*.json                       # Brutos (gitignored)
data/extract.py · data/process_raw.py # Utilitários (gitignored)
.gitignore
CHANGELOG.md                          # Histórico de mudanças de dados
roadmap.md                            # Sprints futuras
brasil_transparente_painel_bandeira.html  # CANÔNICO (v1.2+)
_legacy/                              # Arquivos históricos (commitado, preserva histórico)
    brasil_em_numeros_dark.html
    brasil_em_numeros_dark_copia.html
    brasil_no_bolso.html
    brasil_no_bolso_copia.html
    brasil_transparente_exploratorio_v1.html   # v1 experimental (ITD, busca, locked cards)
```

## Endpoints

### Siconfi (fetch direto, server-side)
```
GET https://apidatalake.tesouro.gov.br/ords/siconfi/tt/rreo
  ?an_exercicio={ano}&nr_periodo={P}&co_tipo_demonstrativo=RREO&id_ente={ibge}
```

**Schema:**
- `items[].exercicio`, `instituicao`, `cod_ibge`, `uf`, `populacao`
- `items[].anexo` — sempre filtrar por `"RREO-Anexo 01"` para receita/despesa resumidas
- `items[].coluna` — `"PREVISÃO INICIAL"`, `"PREVISÃO ATUALIZADA (a)"`, `"Até o Bimestre (c)"`, `"DOTAÇÃO INICIAL (d)"`, `"DOTAÇÃO ATUALIZADA (e)"`, `"DESPESAS EMPENHADAS ATÉ O BIMESTRE (f)"`, etc.
- `items[].cod_conta` — `"ReceitasExcetoIntraOrcamentarias"` ou `"DespesasExcetoIntraOrcamentarias"`
- `items[].valor` — número em reais

**Códigos IBGE dos 6 estados atuais:**
- SP=35, MG=31, RJ=33, BA=29, PR=41, RS=43

### raw.githubusercontent.com (fetch do browser)
```
GET https://raw.githubusercontent.com/speedvarginha-coder/brasil-transparente/main/data/{uf}.json
```

CORS liberado. Sem necessidade de token.

## Convenções do código

### HTML canônico (`brasil_transparente_painel_bandeira.html`)

- Auto-contido. Pode ser aberto direto com `file://`.
- CSS no `<style>` interno, JS no `<script>` interno (no fim do body).
- IDs em camelCase.
- Constantes globais: `CONFIG={...}`, `estados=[...]`, `ibgeCodes={...}`, `REPO_OWNER='speedvarginha-coder'`, `REPO_BRANCH='main'`.
- Funções utilitárias: `brl()`, `short()`, `secondsSinceYearStart()`, `find()`.
- Handlers `init`: registrados no fim do script + invocados na ordem certa.

### JSON de snapshot
```json
{
  "uf": "SP",
  "nome": "Governo do Estado de São Paulo",
  "codigoIbge": 35,
  "fonte": "Siconfi - Tesouro Nacional",
  "demonstrativo": "RREO",
  "exercicio": 2023,
  "periodo": 6,
  "periodicidade": "Bimestral",
  "dataColeta": "2026-06-26T...",
  "urlOriginal": "https://apidatalake.tesouro.gov.br/ords/siconfi/tt/rreo?...",
  "populacao": 46649132,
  "receitaPrevisaoInicial": 317408397614,
  "receitaPrevisaoAtualizada": 309832419357.9,
  "receitaRealizada": 309232504037.6,
  "despesaDotacaoInicial": 317408397614,
  "despesaDotacaoAtualizada": 329593817989.69,
  "despesaEmpenhada": 310805537272.25,
  "despesaLiquidada": ...,
  "despesaPaga": ...
}
```

## Workflow de mudança

### Adicionar novo indicador
1. Editar `CONFIG={...}` no HTML.
2. Adicionar card no HTML com badge de fonte.
3. Atualizar `Tabela Cidadã` se for KPI grande.
4. Atualizar `Compromisso com o dado` se for princípio novo.
5. Incrementar versão em `dataVersion` no rodapé (`v1.x`).
6. Adicionar entrada no `CHANGELOG.md`.
7. Commit + push.

### Adicionar novo estado
1. Adicionar código IBGE em `ibgeCodes` no HTML.
2. Adicionar objeto em `estados` array com valores hardcoded (fallback).
3. Adicionar UF em `scripts/fetch_siconfi.py` no dict `UFS`.
4. Rodar `python scripts/fetch_siconfi.py {uf}` localmente.
5. Commit + push → Action valida end-to-end.

### Atualizar Action manualmente
1. Ir em https://github.com/speedvarginha-coder/brasil-transparente/actions
2. Workflow "Update Siconfi data" → Run workflow
3. Opcionalmente filtrar por UF.

## Decisões registradas

- **Sprint 1 (26/06/2026):** Credibilidade visível — badges de fonte, compromisso com o dado, CHANGELOG.
- **Sprint 2 (26/06/2026):** Fonte por KPI — série histórica Dívida/PIB, 6 estados reais, CSV download.
- **v1.1.1 (26/06/2026):** Integração Tesouro Transparente — seção "Onde ver os números oficiais".
- **v1.1.2 (26/06/2026):** Protótipo fetch Siconfi — função `fetchEstadoSiconfi()` com tratamento CORS.
- **v1.2 (26/06/2026):** Arquitetura JSON cacheado — GitHub Action mensal + raw.githubusercontent.com.

## Pendências conhecidas

- **v1.html experimental:** ✅ arquivado em `_legacy/brasil_transparente_exploratorio_v1.html` em 2026-06-26.
- **Modal de indicador:** planejado Sprint 3.
- **Cada R$ 100 com LOA real:** planejado Sprint 3.
- **Judiciário com CNJ:** planejado Sprint 3.
- **Glossário cidadão:** identificado em `_legacy/brasil_transparente_exploratorio_v1.html` (conceito do ITD, busca local, locked cards).

## Notas operacionais

### Push
```bash
git add .
git commit -m "mensagem"
git push origin main
```
Credenciais já configuradas via Git Credential Manager do Windows. Push sem pedir senha.

### Encoding
PowerShell 5.1 `-Encoding utf8` pode gerar double-encoding em alguns casos. Sintoma: caracteres acentuados aparecem como `Sǜo Paulo` em vez de `São Paulo`. Workaround Python: ler bytes, decodar latin1, re-decodar utf-8.

### Permissões do bash
Algumas operações (push, fetch com `Remove-Item`) requerem aprovação explícita. Operações read-only são automáticas.

## Contato

Projeto pessoal de [@speedvarginha-coder](https://github.com/speedvarginha-coder). Sem issues abertas. Sem Pull Requests.
