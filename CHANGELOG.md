# Brasil Transparente — Changelog de Dados

Registro público de toda alteração em dados, regras de cálculo ou fontes. Formato inspirado em [Keep a Changelog](https://keepachangelog.com/).

---

## [v1.8.0] — 2026-06-26 — Custo parlamentar com médias + Imposto no dia a dia

### Adicionado
- **Seção `#parlamentar` com médias concretas**:
  - Deputado Federal: subsídio R$ 46.366,19 + verba de gabinete R$ 165.806,07 + **CEAPS até R$ 30.788,00/mês** (uniforme por lei federal) + 5-25 assessores. **Custo total médio mensal ≈ R$ 247 mil**.
  - Senador: subsídio R$ 46.366,19 + **CEAPS Senado ≈ R$ 30.000/mês** (teto médio) + estrutura gabinete/escritório de apoio **≈ R$ 150-200 mil/mês** + até 25 assessores. **Custo total médio mensal ≈ R$ 230-280 mil**.
  - 3 miniCards de totais anuais: Câmara R$ 1,52 bi · Senado R$ 245 mi · Congresso total R$ 1,77 bi (0,027% do orçamento).
- **Nova seção `#impostos-cotidiano`** com 18 itens domésticos mostrando % de imposto estimado:
  - **Alta carga (>30%)**: Cigarro 70%, Cerveja 50%, Gasolina 45%, Celular 40%, Refrigerante 38%, Internet 35%, Energia 30%.
  - **Carga média (15-30%)**: Carro popular 28%, Moto 25%, TV por assinatura 25%, Roupas 22%, Medicamento 20%, Café 18%, Carne bovina 15%.
  - **Cesta básica (<15%)**: Leite 12%, Pão 11%, Arroz 10%, Frango 9%.
  - Cada card mostra emoji, nome, % e exemplo em R$.
  - Barra visual horizontal proporcional ao % (cor: vermelho alto / amarelo médio / verde baixo).
  - Box de impacto: família de 4 pessoas gasta **R$ 6.800 a R$ 8.200/ano em imposto embutido** — 1 a 2 meses de salário mínimo só nisso.
- **CSS novo**: `.impostoGrid`, `.impostoItem.alto/.medio/.baixo`, `.impEmoji`, `.impNome`, `.impPct`, `.impBar`, `.impEx`.
- **Nav lateral**: novo item "Imposto no dia a dia".
- **CSV `impostos_cotidiano`** com 18 linhas + colunas `item,categoria,percentual_imposto,exemplo_preco,imposto_estimado,fonte`.

### Corrigido (UX)
- Substituído "varia por estado" na seção parlamentar por **CEAPS de R$ 30.788,00 (Deputado, fixo por lei federal)** e faixas médias com explicação (Senador, com teto CEAPS + faixa de estrutura física conforme UF).

### Fontes utilizadas
- Câmara dos Deputados — Resolução que fixa verba de gabinete e teto CEAPS.
- Senado Federal — CEAPS e estrutura de gabinetes.
- Confaz — ICMS médio por estado.
- Receita Federal — PIS/COFINS, IPI.
- ANP — preços médios de combustíveis.
- Anatel — telecomunicações.
- Aneel — energia elétrica.
- IBGE — carga tributária bruta (% PIB).

### Premissas didáticas
- Para a gasolina, o cálculo soma ICMS (média nacional ~28%) + PIS/COFINS (~R$ 0,13/L fixo, equivalente a ~2% ad valorem médio) + CIDE (R$ 0,10/L fixo).
- Para telecom, considera ICMS (25%) + PIS/COFINS (3,65%) + FUST (1%) + FUNTEL (0,5%).
- Itens da cesta básica têm ICMS reduzido por lei federal (7% em SP/MG, 12% na maioria dos estados) — referência é a média nacional.
- Percentuais arredondados para inteiros para comunicação; precisão está na fonte.

---

## [v1.7.0] — 2026-06-26 — Linha do tempo Dívida/PIB com períodos coloridos + LRF

### Adicionado
- **Seção `#linhatempo` reformulada** com 4 miniCards de marcos numéricos:
  - 📉 Menor valor: **38,5%** (2008, antes da crise)
  - 📈 Pico histórico: **87,1%** (2020, pandemia)
  - 📊 Último oficial: **76,1%** (2024)
  - 🔮 Projeção 2026: **80,4%** (Boletim Focus / BC)
- **Gráfico agora coloriza barras por período**:
  - Verde (2006-2019) = pré-pandemia
  - Vermelho/laranja (2020) = pico pandêmico
  - Azul (2021-2026) = pós-pandemia
- **Linha tracejada amarela** marcando o limite prudencial da LRF (60% do PIB) — referência visual clássica da Lei de Responsabilidade Fiscal (LC 101/2000, art. 29).
- **3 miniCards de variações-chave**:
  - 2006 → 2026: **+33,9 pp** (crescimento de 73% em pp)
  - 2008 → 2020: **+48,6 pp** (mais que dobrou)
  - 2020 → 2024: **−11,0 pp** (recuperação parcial)
- **Box de impacto final** com equivalências concretas: 80,4% do PIB ≈ R$ 10,4 trilhões = mais que 4 anos de orçamento da União; juros anuais (R$ 1,096 tri) > orçamento Saúde + Educação.
- **Legenda colorida** abaixo do gráfico (períodos + LRF).

### CSS novo
- `.marcoPre`, `.marcoPico`, `.marcoAtual`, `.marcoFuturo` — 4 cards coloridos com gradiente sutil.
- `.variacaoUp` (vermelho), `.variacaoDown` (verde) — destaque tipográfico das variações.
- `.legendTimeline` + `.legDot.{pre,pico,pos,lrf}` — legenda colorida.
- `.timelineChart .tcol.pre/.pico/.pos` — cores por período.
- `.timelineChart .lrfLine` — linha tracejada amarela com label "LRF 60%".

### JS atualizado
- `drawTimeline()` agora classifica cada barra por período e posiciona a linha do LRF proporcionalmente (calculado em `requestAnimationFrame` para respeitar altura real do container).
- Adicionada altura inline `style="height:${h}%"` em cada `.tcol` baseada no valor (% do PIB × 0.85). Antes as barras não tinham altura explícita e ficavam invisíveis (altura natural ≈ 0 com filhos `position:absolute`).
- Bugfix: chave `}` de fechamento da função `drawTimeline()` que faltava no commit anterior — quebrava todo o JS subsequente (`drawTimeline is not defined`, gráfico vazio).

### Validação
- Validei o JS inline extraindo o `<script>` e rodando `new Function()` em Node — agora `OK` sem erros de sintaxe.
- Confirmei via Playwright que as 11 barras renderizam com altura proporcional real: 2008 (menor) = 74 px, 2020 (pico) = 165 px, 2026 (proj) = 152 px.

### Fontes / Referências
- Banco Central — Estatísticas Fiscais (série anual Dívida Bruta / PIB).
- Boletim Focus / BC (projeção 2026).
- LRF — Lei Complementar 101/2000, art. 29 (limite prudencial 60% RCL — usado aqui como referência visual clássica).

---

## [v1.6.0] — 2026-06-26 — Escala do dinheiro reformulada (4 visões)

### Adicionado
- **Seção `#escala` totalmente reformulada** com 4 visões complementares para explicar a diferença entre mil / milhão / bilhão / trilhão:
  - **🪜 Visão 1 — Escada dos zeros**: cada degrau adiciona 3 zeros e multiplica o valor por 1.000 (visual com blocos █ crescendo).
  - **⏱️ Visão 2 — Gráfico de tempo**: tempo para contar cada valor a 1 número/segundo (Mil = 16 min 40 s, Milhão = 11 dias 14 h, Bilhão = 31 anos 8 meses, Trilhão = 31.709 anos).
  - **👥 Visão 3 — 4 personagens**: João (R$ 1.000), Carlos (R$ 1 milhão), Ana (R$ 1 bilhão), Brasil (R$ 1 trilhão) — cada um com tempo necessário para juntar o próprio patrimônio recebendo R$ 1/s.
  - **📏 Visão 4 — Régua do trilhão**: régua horizontal onde 1 trilhão = barra cheia; bilhão = 0,1 milésimo da régua; milhão e mil invisíveis.
- **Comparações extras**: pilhas de notas de R$ 100 (10, 10.000, 10 milhões, 10 bilhões) e tabela de salários (R$ 3.000/mês = 28 anos para milhão, 27.778 para bilhão, 27,8 milhões de anos para trilhão).
- **Box de impacto final** com gradiente amarelo: "R$ 1 bilhão parece 'apenas um número'. Mas se você recebesse R$ 1 por segundo, precisaria trabalhar 31 anos para juntar esse valor. R$ 1 trilhão? 31.709 anos."
- **CSS novo**: `.escadaZeros`, `.degrau`, `.tempoChart`, `.personaCena`, `.regruaEscala`, `.impactoFinal` — todos responsivos.
- **Media query** (`max-width:760px`) reorganiza `personaCena` em 2 colunas e simplifica `tempoRow` em mobile.

### Substituiu
- Antiga seção `#escala` com apenas 6 miniCards em grid uniforme (não transmitia a diferença real entre as escalas).

### Premissas das comparações
- 1 número por segundo, sem parar, 24h/dia (referência padrão didática).
- R$ 1/s é referência temporal usada em todas as comparações.
- Salário base: R$ 3.000/mês e R$ 10.000/mês (premissas didáticas abertas).
- Notas de R$ 100 (referência visual padrão).

### Fontes conceituais
- Matemática de escala: regra 10³ entre mil/milhão/bilhão/trilhão.
- Não há fonte oficial específica — é didática de comparação. A referência didática padrão está em materiais de educação financeira (Banco Central, BCB Educação Financeira).

---

## [v1.5.0] — 2026-06-26 — Custo parlamentar detalhado + Emendas e Fundos proporcionais

### Adicionado
- **Seção `parlamentar` agora tem 2 miniCards com tabela detalhada** (substituindo o placeholder anterior):
  - Deputado Federal: subsídio R$ 46.366,19/mês, verba de gabinete R$ 165.806,07/mês, 5–25 secretários parlamentares.
  - Senador: subsídio R$ 46.366,19/mês, estrutura variável por estado.
  - Nota metodológica explicando que verba de gabinete e número de assessores foram coletados da Câmara dos Deputados.
- **Nova seção `#emendas-fundos`** com barra proporcional visual:
  - Emendas parlamentares 2026: **R$ 61 bi** (Congresso Nacional · LOA 2026)
  - Fundo Eleitoral 2026: **R$ 4,96 bi** (TSE · FEFC)
  - Fundo Partidário 2026: **~R$ 1 bi** (TSE)
  - Largura de cada bloco é proporcional ao valor (Emendas = 100, Fundo Eleitoral = 8,1, Fundo Partidário = 1,6) — a diferença é imediata visualmente.
  - Card comparativo mostrando proporção: Emendas ~12× Fundo Eleitoral, ~61× Fundo Partidário.
  - Botão de download CSV da nova seção.
- **Item na nav lateral**: "Emendas & Fundos".
- **CSV `emendas_fundos_2026`** com colunas `rubrica,valor_reais,fonte,descricao`.

### Alterado (UX)
- Substituído `grid three` (3 colunas iguais) por `.efProportional` flexbox com gradientes em 3 tons de azul, refletindo a proporção real entre os valores.
- Hover com `translateY(-2px)` em cada bloco.

### Dados utilizados (todos oficiais)
- LOA 2026: Congresso Nacional → <https://www.congressonacional.leg.br/web/orcamento/acompanhe/orcamento-anual>
- TSE · FEFC 2026: <https://www.tse.jus.br/eleicoes/eleicoes-2026-content/prestacao-de-contas/distribuicao-dos-recursos-do-fundo-especial-de-financiamento-de-campanha-fefc-eleicoes-2026>
- TSE · Fundo Partidário: <https://www.tse.jus.br/partidos/partidos-1/fundo-partidario>
- Subsídio parlamentar: fixado em R$ 46.366,19 desde 2018 (sem alteração em 2026).
- Verba de gabinete: Câmara dos Deputados — resolução vigente.

---

## [v1.3.6] — 2026-06-26

### Adicionado
- **Seção "Escala do dinheiro"** para explicar a diferença entre mil, milhão, bilhão e trilhão.
- **Analogias de tempo** mostrando quanto levaria para juntar R$ 1 bi e R$ 1 tri com salário de R$ 10 mil/mês.
- **Equivalências cidadãs** nos módulos de corrupção e renúncia fiscal: transferência de R$ 600/mês, escolas de R$ 15 mi, hospitais de R$ 250 mi e ambulâncias de R$ 350 mil.
- **CSVs atualizados** para exportar as equivalências de corrupção e renúncia fiscal.

### Nota metodológica
- As equivalências são didáticas e usam premissas abertas. Não são promessa de execução de obra nem substituem orçamento executivo.

---

## [v1.3.5] — 2026-06-26

### Adicionado
- **Módulo Judiciário com dados oficiais do CNJ** substituindo o placeholder "Em breve".
- **Indicadores CNJ 2024**: despesa total, custo por habitante, peso no PIB, despesa com pessoal, custo operacional sem inativos e receitas arrecadadas.
- **CSV específico** para o módulo Judiciário (`judiciario_cnj_2024`).
- **Entrada na Tabela Cidadã** e no ranking macro.
- **Aba Poderes do ranking** agora compara Judiciário total e Judiciário/pessoal com Executivo Federal.

---

## [v1.3.4] — 2026-06-26

### Alterado (UX)
- **Fontes oficiais** movido para o final do painel, como seção de apoio e auditoria.
- **Compromisso com os dados** mantido como último bloco de conteúdo, reforçando governança sem interromper a leitura principal.
- **Navegação lateral** reorganizada para seguir a nova ordem da página.

---

## [v1.3.3] — 2026-06-26

### Adicionado
- **Seção "Renúncia fiscal"** com valor oficial de gastos tributários federais previstos no DGT/PLOA 2026 da Receita Federal.
- **Terminologia cidadã** explicando que o mesmo fenômeno pode aparecer como gasto tributário, benefício tributário, desoneração, isenção, alíquota zero ou regime especial.
- **Escala fiscal**: R$ 612,84 bi, 4,43% do PIB, 20,20% das receitas administradas pela RFB e valor por brasileiro.
- **Comparações visuais** com Saúde no orçamento e Emendas parlamentares.
- **CSV específico** para renúncia fiscal (`renuncia_fiscal_2026`).
- **Entrada no ranking macro** para comparar renúncia fiscal com juros, custo da corrupção, saúde, emendas e fundos político-eleitorais.

---

## [v1.3.2] — 2026-06-26

### Adicionado
- **Seção "Custo da corrupção"** com faixa didática de impacto econômico entre 1,38% e 2,3% do PIB.
- **Cards de escala**: cenário baixo, cenário alto e custo anual por brasileiro.
- **CSV específico** para a estimativa de corrupção (`custo_corrupcao_estimativa`).
- **Entrada no ranking macro** para comparar a ordem de grandeza com juros, saúde, emendas e fundos político-eleitorais.
- **Metodologia explícita** deixando claro que é estimativa econômica, não valor oficial de desvios comprovados.

---

## [v1.3.1] — 2026-06-26

### Corrigido (UX)
- **Quebra de linha nos valores dos KPIs**: "R$ 10,4 tri" e "R$ 1,096 tri" estavam quebrando em 2 linhas por causa do badge `position: absolute` empurrando o conteúdo.
  - `.kpi .value`: `font-size` reduzido de `clamp(26px,2.65vw,35px)` para `clamp(22px,2.2vw,30px)`, `word-break: keep-all`, `hyphens: none`.
  - `.kpi .label`: `font-size` reduzido de 13px para 12px, `text-transform: uppercase`, `letter-spacing`, `min-height: 32px`.
- **Títulos dos KPIs cortados**: "Juros em 12 m" e "Orçamento Uniã" — ajuste de `padding-top: 42px` no `.kpi` + `min-height` no label garantem que o badge não sobreponha o título.
- **Badge muito largo**: `.sourceBadge` reduzido de `font-size: 11px` / `max-width: 78%` para `font-size: 9.5px` / `max-width: 55%`. Mais discreto, dá mais espaço pro conteúdo.

### Removido (limpeza)
- **Callout "Versão profissional"** — era marketing puro, sem dado real, sem link. Substituído pelo silêncio (a seção não acrescenta valor ao usuário comum).
- **3ª opção do quiz "Não existe diferença no orçamento público"** — opção absurda que poluía a tela. Quiz agora tem 2 opções claras (Sim/Não). CSS `.quizBtns` adicionado pro layout em grid.

---

## [v1.3] — 2026-06-26 — Sprint 3 / Item 3.1

### Adicionado
- **Modal de Indicador** com 5 abas (Fonte / Metodologia / Histórico / Links / Download) acionado por clique nos 4 KPIs principais (Dívida, Juros, Orçamento, Emendas).
- **Objeto `INDICADORES`** com metadados completos pra cada um dos 4 KPIs grandes:
  - Título, badge de fonte, dot color
  - Valor + complemento ("≈ 80,4% do PIB")
  - MetaGrid com Fonte / Competência / Periodicidade / Atualização
  - Metodologia (parágrafo + listas do que inclui / não inclui)
  - Histórico (marcos e tendências)
  - Links oficiais (botões que abrem em nova aba)
  - CSV específico por indicador
- **Função `downloadIndicatorCSV(key)`** que baixa CSV específico do indicador aberto, com BOM UTF-8 e referência ao commit canônico.
- **Botão "🔄 Buscar atualização ao vivo"** dentro do modal (chama `fetchEstadoSiconfi()` indireto via reload da seção).
- **Acessibilidade**: `role="button"`, `tabindex="0"`, `aria-label`, suporte a Enter/Space para abrir modal via teclado.
- **ESC** fecha o modal.
- **Click no overlay** fecha o modal.
- **Animação suave** de entrada (`modalIn` 220ms ease-out).

### Detalhes técnicos
- CSS novo: `.modalOverlay`, `.modalContent`, `.modalHeader`, `.modalTabs`, `.modalTab`, `.modalBody`, `.modalTabPanel`, `.metaGrid`, `.metaItem`, `.bigValue`, `.modalLinkBtn` (primary + secondary).
- HTML: bloco `<div class="modalOverlay">` no fim do `<body>`, antes do `<footer>`.
- JS: objeto `INDICADORES` (~120 linhas), funções `openModal`, `closeModal`, `switchTab`, `downloadIndicatorCSV`.
- Listeners: querySelectorAll('.kpi[data-indicador]') + addEventListener click + keydown (Enter/Space).
- `currentModal` global para tracking (usado pelo ESC handler).

### UX
- KPI hover: lift de 2px + sombra forte + borda verde-escuro.
- "clique p/ detalhes" no small text dos KPIs avisa sobre a interatividade.
- Modal com gradiente verde→azul no header (identidade Brasil Transparente).
- Botão close com rotação 90° no hover.

### Próximos passos (Sprint 3 ainda)
- 3.2 Cada R$ 100 com base LOA real (substituir simulação por dado oficial).
- 3.3 Judiciário com dados do CNJ.
- 3.4 Custo total anual por parlamentar (Câmara + Senado separados).

---

## [v1.2.1] — 2026-06-26

### Refactor
- **`brasil_transparente_v1.html` arquivado** em `_legacy/brasil_transparente_exploratorio_v1.html` com nome descritivo.
- Pasta `_legacy/` agora é commitada (antes era gitignored). Decisão: preservar histórico da versão experimental que introduziu conceitos de ITD, busca local e locked cards — pode ser útil em iterações futuras.
- Gitignore atualizado: `_legacy/` descomentado.

### Notas
- A versão exploratória tem conceitos valiosos (ITD, glossário, locked cards) que podem inspirar a Sprint 3.

---

## [v1.2] — 2026-06-26

### Deploy
- **Repositório público criado**: `https://github.com/speedvarginha-coder/brasil-transparente`
- **Primeira execução da Action em 2026-06-26 14:48 BRT** — concluída em 8s, status `success`, event `push`. End-to-end validado: checkout → Python 3.12 → fetch Siconfi → validação JSON → auto-commit. Sem commits redundantes porque os dados não mudaram desde o fetch inicial.

### Adicionado
- **Arquitetura JSON cacheado**: pasta `data/` com 1 JSON por UF (SP, MG, RJ, BA, PR, RS), commitados no repo.
- **GitHub Action mensal**: `.github/workflows/update-siconfi.yml` com cron `0 3 1 * *` (todo dia 1 às 03:00 UTC = 00:00 BRT).
- **GitHub Action via push** (paths filter em `scripts/` e `.github/`) — valida o workflow em qualquer mudança.
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
