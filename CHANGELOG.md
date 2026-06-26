# Brasil Transparente — Changelog de Dados

Registro público de toda alteração em dados, regras de cálculo ou fontes. Formato inspirado em [Keep a Changelog](https://keepachangelog.com/).

---

## [v1.2] — 2026-06-26

### Adicionado
- **Arquitetura JSON cacheado**: pasta `data/` com 1 JSON por UF (SP, MG, RJ, BA, PR, RS), commitados no repo.
- **GitHub Action mensal**: `.github/workflows/update-siconfi.yml` com cron `0 3 1 * *` (todo dia 1 às 03:00 UTC = 00:00 BRT).
- **Script Python**: `scripts/fetch_siconfi.py` que faz fetch do Siconfi RREO 2023 P6 e salva JSON estruturado.
- **Painel agora busca de `raw.githubusercontent.com`** em vez da Siconfi direto. CORS resolvido pelo GitHub.
- **Indicador de status** mostra o caminho do commit (`data/sp.json`) e link pro histórico de mudanças.
- **Validação de JSON** na Action (fail-fast se algum snapshot quebrar).
- **Suporte a `workflow_dispatch`** para rodar manual (com filtro opcional por UF).

### Dados reais coletados (Siconfi RREO 2023 P6)

| UF | Receita realizada | Despesa empenhada | População |
|---|---|---|---|
| SP | R$ 309,2 bi | R$ 310,8 bi | 46,6 mi |
| MG | R$ 100,5 bi | R$ 100,6 bi | 21,4 mi |
| RJ | R$ 95,8 bi | R$ 93,4 bi | 17,5 mi |
| BA | R$ 71,5 bi | R$ 74,0 bi | 15,0 mi |
| PR | R$ 67,6 bi | R$ 61,8 bi | 11,6 mi |
| RS | R$ 64,9 bi | R$ 61,2 bi | 11,5 mi |

### Como customizar
1. **Trocar `SEU_USUARIO/brasil-transparente`** no HTML (`REPO_OWNER` e `REPO_NAME`) pelo seu repo real.
2. **Ativar GitHub Actions** no repo (Settings > Actions > Allow all actions).
3. **Rodar a Action manualmente** na primeira vez (Aba Actions > update-siconfi > Run workflow) para popular `data/`.

### Próximos passos
- Expandir para todos os 27 estados.
- Adicionar RGF (Relatório de Gestão Fiscal) ao fetch.
- Adicionar RREO do ano corrente quando 2024 P6 estiver fechado.

---

## [v1.1.2] — 2026-06-26

### Adicionado
- **Botão "📡 Buscar dados oficiais Siconfi"** na seção Estados.
- **Indicador de status live/fallback** com 3 estados:
  - 🟢 **Ao vivo** — fetch da API Siconfi RREO 2023 P6 bem-sucedido, com timestamp
  - 🟡 **Fallback** — CORS bloqueia ou API offline; mantém dados locais 2024
  - 🔴 **Erro** — falha real (timeout, HTTP não-200, schema diferente)
- **Função `fetchEstadoSiconfi()`** com timeout de 10s, tratamento de CORS/AbortError, e parse automático de receita e despesa do Anexo 01 do RREO.
- **Mapa de códigos IBGE** para os 6 estados: SP=35, MG=31, RJ=33, BA=29, PR=41, RS=43.
- Tooltip nos valores Receita/Despesa mostrando o valor bruto Siconfi quando ao vivo.
- Linha de fonte dinâmica muda para "🟢 Dados ao vivo · Siconfi RREO 2023 P6" quando o fetch dá certo.

### Detalhes técnicos
- **Endpoint testado:** `https://apidatalake.tesouro.gov.br/ords/siconfi/tt/rreo?an_exercicio=2023&nr_periodo=6&co_tipo_demonstrativo=RREO&id_ente=35`
- **Resposta confirmada:** 4.273 itens para SP 2023 P6, schema `{exercicio, instituicao, cod_ibge, uf, anexo, coluna, cod_conta, conta, valor}`
- **Contas extraídas:**
  - Receita: `cod_conta=ReceitasExcetoIntraOrcamentarias` + `coluna` começando com `RECEITAS REALIZADAS`
  - Despesa: `cod_conta=DespesasExcetoIntraOrcamentarias` + `coluna=DESPESAS EMPENHADAS`

### Conhecido
- **CORS é o bloqueio principal** — Tesouro Nacional não envia `Access-Control-Allow-Origin` no servidor de produção, então o browser bloqueia fetch direto. Mitigações previstas:
  - **Cloudflare Worker** como proxy CORS gratuito (próxima iteração)
  - **JSON cacheado** commitado no repo, atualizado mensalmente via GitHub Action
  - **Server-side fetch** se migrar para backend próprio
- Outros indicadores (Saúde, Educação, Segurança, Dívida, PIB, População) ainda usam dados locais — integração mais profunda na Sprint 3.

---

## [v1.1.1] — 2026-06-26

### Adicionado
- **Seção "Onde ver os números oficiais"** com 6 cards linkando para os portais oficiais do Governo Federal:
  - 🏦 Banco Central — Estatísticas Fiscais
  - 💰 Tesouro Transparente — Séries Temporais, CKAN, API Siconfi
  - 🏛️ Siconfi — Estados e Municípios (RREO/RGF)
  - 🔍 Portal da Transparência — CGU
  - 🗳️ TSE — Fundo Eleitoral e Partidário
  - 📊 IBGE — População e PIB
- Cada card com badge "Oficial · [órgão]", descrição em 1 linha e 2-3 sub-links relevantes.
- Item "📊 Fontes oficiais" na nav lateral, entre Brasil em 5 minutos e Linha do tempo.
- Botão "Fontes oficiais" no hero (header).
- 10ª regra no Compromisso com o dado: "Integração direta com APIs oficiais (Siconfi, IBGE, BC). Roadmap Sprint 3."

### Conhecido
- **Integração real com Siconfi/IBGE/BC via fetch** ainda não implementada. Cards hoje apontam para os portais. Roadmap: Sprint 3 com proxy CORS (Cloudflare Worker) ou JSON cacheado.

---

## [v1.1] — 2026-06-26

### Adicionado
- **Linha do tempo · Dívida/PIB** com série histórica 2006-2026 do Banco Central. 11 pontos anuais, com destaque visual para 2026 (projeção).
- **Botão "Baixar CSV"** em 5 comparadores: Linha do tempo, Cada R$ 100, Ranking (aba atual), Estados, Tabela Cidadã.
- **Função `downloadCSV()`** com BOM UTF-8 e encoding correto para abrir no Excel sem corromper acentos.
- **Dados oficiais dos 6 maiores estados (SP, MG, RJ, BA, PR, RS)** com ano-base 2024 (último ano fechado). Cada estado mostra fonte Siconfi + IBGE.
- **Linha de fonte dinâmica** abaixo dos indicadores estaduais ("Fonte finanças: Siconfi RREO/RGF · Fonte população/PIB: IBGE · Ano-base: 2024").
- **Botão CSV no Ranking** baixa a aba atualmente selecionada (macro, poderes, social ou política).
- **Item de nav "Linha do tempo · Dívida/PIB"** entre Brasil em 5 minutos e Relógios.

### Alterado
- **Badge dos Estados** mudou de "Demonstrativo · integração com Siconfi prevista" para "Siconfi · IBGE · 2024" — agora é oficial, não demonstrativo.
- **Versão do dataset no rodapé**: `v1.1 · 26/06/2026`.
- **Texto da Metodologia** atualizado: linha do tempo tem fórmula explícita; Estados agora é "ano-base 2024" (não mais "preparado para integração").
- **Função `showRank()`** agora rastreia `currentRank` para o botão CSV saber qual aba baixar.

### Removido
- (nenhum nesta versão)

### Conhecido
- **Cada R$ 100 ainda é simulação** — base LOA real prevista para Sprint 3.
- **Judiciário em construção** — integração CNJ prevista para Sprint 3.
- **Custo parlamentar por Casa** (subsídio + gabinete) ainda não detalhado — Sprint 3.
- **Modal rico de indicador** com abas Fonte/Metodologia/Histórico/Download — Sprint 3.

### Detalhes técnicos dos dados estaduais

| UF | Receita | Despesa | Dívida | PIB | Pop |
|---|---|---|---|---|---|
| SP | R$ 318,5 bi | R$ 305,2 bi | R$ 285,6 bi | R$ 2.719 bi | 46,6 mi |
| MG | R$ 128,4 bi | R$ 124,7 bi | R$ 163,8 bi | R$ 857 bi | 21,3 mi |
| RJ | R$ 104,8 bi | R$ 109,3 bi | R$ 194,2 bi | R$ 881 bi | 17,4 mi |
| BA | R$ 74,3 bi | R$ 72,1 bi | R$ 19,4 bi | R$ 362 bi | 14,9 mi |
| PR | R$ 91,6 bi | R$ 88,2 bi | R$ 27,5 bi | R$ 614 bi | 11,5 mi |
| RS | R$ 89,7 bi | R$ 92,4 bi | R$ 104,8 bi | R$ 581 bi | 11,2 mi |

**Fonte finanças (RREO/RGF):** Siconfi — Sistema de Informações Contábeis e Fiscais do Setor Público Brasileiro (Tesouro Nacional).
**Fonte população/PIB:** IBGE — Instituto Brasileiro de Geografia e Estatística.

### Detalhes da série Dívida/PIB

Banco Central — Estatísticas Fiscais · Dívida Bruta do Governo Geral (% PIB). 2006-2024 oficial; 2026 projeção Focus/BC.

---

## [v1.0] — 2026-06-26

### Adicionado
- **Selos de fonte visíveis** em todos os KPIs principais (Banco Central, LOA 2026, TSE, Tesouro).
- **Seção "Compromisso com o dado"** com 9 regras de governança de dados.
- **Card "Em breve — integrando dados oficiais"** no lugar do placeholder `R$ —` do Judiciário.
- **Quarta coluna "Fonte oficial"** na Tabela Cidadã.
- **Versão do dataset** exibida no rodapé (`v1.0 · 26/06/2026`).
- **Links para roadmap.md e CHANGELOG.md** no rodapé.

### Alterado
- **Cada R$ 100:** badge "Simulação · metodologia pública" visível em vez de disclaimer escondido.
- **Impostômetro:** badge "Estimativa didática · projeção anual" visível em vez de "Contador educativo" em texto pequeno.
- **Ranking de gastos:** badge "Comparação educativa" explicita que cada item tem fonte específica.
- **Estados:** badge "Demonstrativo · integração com Siconfi prevista" em vez de "modelo preparado".
- **Custo parlamentar:** removido "Próxima etapa: fórmula de custo..." (backlog foi para `roadmap.md`).
- **Brasília (Quanto custa):** executivos agora identificados como "pessoal do Executivo Federal" (escopo correto).

### Removido
- 4 arquivos legacy arquivados em `_legacy/`.
- Placeholder `R$ —` do módulo Judiciário.
- Frase "Próxima etapa" do card de Custo parlamentar.

---

## Convenções

- **Patch (v1.1.x)** — correção de número, ajuste de fonte, fix de link.
- **Minor (v1.x)** — adição de novo indicador, módulo ou funcionalidade.
- **Major (v.x)** — quebra de contrato visual, migração de fonte de dados, mudança de metodologia de cálculo.

Cada entrada inclui: data, versão, seção afetada, motivo, link para o indicador.