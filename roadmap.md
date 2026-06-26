# Brasil Transparente — Roadmap

Itens fora do produto. Cada item inclui contexto, por que saiu da interface, critério de pronto e estimativa.

---

## Sprints entregues

### ✅ v1.3 — Sprint 3 item 3.1 Modal de Indicador (30 min) — entregue 2026-06-26
- Modal com 5 abas (Fonte / Metodologia / Histórico / Links / Download) acionado por clique nos 4 KPIs principais.
- Objeto `INDICADORES` com metadados completos.
- CSV específico por indicador.
- Acessibilidade: role, tabindex, aria-label, Enter/Space, ESC, click-outside.

### ✅ v1.2 — Arquitetura JSON cacheado (45 min) — entregue 2026-06-26
- **Decisão de arquitetura:** JSON commitado no repo > Cloudflare Worker > backend próprio.
- 6 JSONs em `data/` (SP, MG, RJ, BA, PR, RS) com snapshot RREO 2023 P6 do Siconfi.
- GitHub Action `.github/workflows/update-siconfi.yml` com cron mensal.
- Script `scripts/fetch_siconfi.py` server-side (sem CORS).
- HTML busca do `raw.githubusercontent.com` em vez da Siconfi direto → CORS resolvido.
- Validação JSON na Action (fail-fast).
- README com instruções de setup no CHANGELOG.

### ✅ v1.1.2 — Protótipo fetch Siconfi (30 min) — entregue 2026-06-26
- Botão "Buscar dados oficiais Siconfi" na seção Estados.
- Função `fetchEstadoSiconfi()` com tratamento robusto de CORS/timeout/erro.
- Indicador de status com 3 estados (ao vivo, fallback, erro).
- Endpoint testado e funcionando: RREO 2023 P6 retornou 4.273 itens para SP.
- Mapa IBGE dos 6 estados.
- Bloqueio conhecido: CORS do Tesouro Nacional bloqueia fetch direto no browser.

### ✅ v1.1.1 — Integração Tesouro Transparente (15 min) — entregue 2026-06-26
- Seção "Onde ver os números oficiais" com 6 cards linkando para portais oficiais.
- 10ª regra no Compromisso com o dado (integração API Sprint 3).
- Botão no hero + item na nav.

### ✅ Sprint 1 — Credibilidade visível (1-2h) — entregue 2026-06-26
- 5 arquivos → 1 arquivo canônico + 2 docs de governança. Pasta `_legacy/` com 4 arquivos históricos.
- 12 selos de fonte nos KPIs grandes (Banco Central, LOA 2026, TSE, Tesouro).
- 4ª coluna "Fonte oficial" na Tabela Cidadã.
- Card "Em breve — integrando dados oficiais" no lugar dos placeholders `R$ —` do Judiciário.
- Removido "Próxima etapa" do card de Parlamentar (foi pro roadmap).
- Versão do dataset no rodapé.
- Seção "Compromisso com o dado" no topo da nav.

### ✅ Sprint 2 — Fonte por KPI (meio dia) — entregue 2026-06-26
- **Dados oficiais dos 6 estados** com ano-base 2024 (SP, MG, RJ, BA, PR, RS). Fontes Siconfi (RREO/RGF) + IBGE.
- **Série histórica Dívida/PIB 2006-2026** via Banco Central — 11 pontos anuais, destaque visual para 2026.
- **Botões CSV em 5 comparadores**: Linha do tempo, Cada R$ 100, Ranking, Estados, Tabela Cidadã.
- **Função `downloadCSV()`** com BOM UTF-8 (abre limpo no Excel).

---

## Sprint 3 — Modal de indicador (estimativa: 1 dia)

### 3.1 — Modal rico por indicador
- **Hoje:** usuário que clica num KPI cai em lugar nenhum.
- **Critério de pronto:** modal com 5 abas — Fonte / Metodologia / Histórico / Link oficial / Download.
- **Justificativa do modal vs link externo:** dá pra empilhar referência + dado + cálculo sem perder contexto.

### 3.2 — "Cada R$ 100" com base LOA real
- **Hoje:** percentuais fixos no JS (`[['Previdência e assistência',32],['Saúde',12]...]`).
- **Por que não é simples:** LOA não vem com "R$ 100" pronto — precisa agregar por função orçamentária (Previdência, Saúde, Educação…) e subtrair refinanciamento.
- **Critério de pronto:** badge "Oficial · LOA 2026 · Tesouro" em cima; percentuais calculados por função; sem disclaimer "didático".
- **Trabalho estimado:** 1-2 dias pra quem nunca mexeu.

### 3.3 — Judiciário com dados do CNJ
- **Hoje:** card "Em breve".
- **Critério de pronto:** puxar orçamento, magistrados, servidores e custo/habitante do CNJ; exibir com badge e data.

### 3.4 — Custo total anual por parlamentar
- **Hoje:** card tem só a composição (513 + 81).
- **Critério de pronto:** fórmula "orçamento da Casa ÷ parlamentares" aplicada a Câmara e Senado, com fonte oficial.

---

## Sprint 4 — Polimento (estimativa: 1-2 dias)

### 4.1 — Acessibilidade AA
- Contraste AA em todos os textos.
- Navegação por teclado em tudo (incluindo tabs do ranking).
- Leitor de tela com `aria-label` em KPIs e gráficos.
- Foco visível em todos os botões e inputs.

### 4.2 — Citação com anchor + OpenGraph
- Cada card de compartilhamento gera um link com anchor (`#juros`, `#estados`).
- OpenGraph cards por indicador — quando compartilhar no Twitter/WhatsApp aparece imagem rica com o número e fonte.

### 4.3 — Degradação graciosa
- Quando a API oficial cair (Siconfi, BC), painel mostra "última atualização conhecida em DD/MM" e continua exibindo último valor válido.
- Sem quebrar layout, sem tela em branco.

### 4.4 — Cache + data de validade
- Cada KPI grande mostra "Dado válido até DD/MM" além de "Atualizado em".

### 4.5 — Painel por município
- Hoje: 6 estados. Próximo: Municípios via Siconfi.
- Trabalho estimado: 1 semana (precisa de paginação + busca).

### 4.6 — API própria
- Cachear Siconfi/BC/Receita em endpoint próprio, com CORS liberado.
- Permite que outros sites embedem os números.

---

## Backlog (sem data)

- Auditoria externa (parceria com universidade ou OSC de transparência).
- Export PDF por card (workaround atual: print-to-PDF).
- Histórico de votações que afetaram cada indicador.
- App nativo (PWA primeiro, depois nativo).

---

## Decisões registradas

- **2026-06-26 — "Próxima etapa" removido do card de Parlamentar.**
  Por que: backlog não vai pra produção. Vai pra roadmap.
- **2026-06-26 — Placeholders `R$ —` removidos do módulo Judiciário.**
  Por que: placeholder vazio é pior que esconder. Mostra "Em breve — integrando dados do CNJ".
- **2026-06-26 — Painéis legacy arquivados em `_legacy/`.**
  Arquivos: `brasil_em_numeros_dark.html`, `brasil_em_numeros_dark_copia.html`, `brasil_no_bolso.html`, `brasil_no_bolso_copia.html`. Mantidos só pra referência histórica.
- **2026-06-26 — Dados estaduais v1.1 com ano-base 2024 (último ano fechado).**
  Por que: dados de 2025 e 2026 ainda em fechamento pelo Siconfi/RREO. 2024 é o último ano auditável. Atualização mensal via rotina.
- **2026-06-26 — Série Dívida/PIB com 11 pontos anuais (2006-2026).**
  Por que: cobre 4 mandatos presidenciais, pandemia e pós-pandemia — mostra a tendência completa. 2026 marcado como projeção (destaque visual diferente).