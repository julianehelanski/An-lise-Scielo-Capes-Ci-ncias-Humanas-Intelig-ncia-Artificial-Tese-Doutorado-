# Decisões metodológicas — fonte única de verdade

Este arquivo trava os números canônicos da análise bibliométrica. Qualquer divergência entre este documento, o README e outros artefatos do repositório indica desatualização **dos outros artefatos**, não deste. **A tese cita os números desta tabela**, e quando refizermos cálculos atualizamos esta página primeiro.

A motivação para este arquivo: durante a sessão de coleta e processamento, vários relatos narrativos contendo somas manuais introduziram erros aritméticos pontuais (por exemplo, "8 artigos antes de 2021" quando o correto é 23; "2020 × 3" quando o correto é 2020 × 17). Os valores que provêm de operações pandas diretas sobre as planilhas se mantiveram corretos. **Regra adotada:** todo número que vai para a tese sai de operação atômica em pandas (ou da própria contagem nas planilhas via Excel), nunca de soma feita em prosa.

Este documento está organizado em seis blocos: (I) números canônicos CAPES, (II) números canônicos SciELO, (III) comparativo SciELO × CAPES Humanas, (IV) números canônicos OpenAlex, (V) coortes históricas descartadas, (VI) como atualizar.

---

## I. CAPES — Catálogo de Teses e Dissertações 2021–2024

### I.1. Coortes

| Coorte | Definição | N |
|---|---|---:|
| **Universo CAPES total** | Dump oficial `BR-CAPES-BTD-2021A2024-2025-12-01`, 4 XLSX concatenados, sem filtro de tema | **350.071** |
| **Corpus IA/ML/DL** | Aplicação de `utils.classificar_foco_ia` ao universo total | **12.995** |
| └ Foco Central | trabalhos com termo de IA stricto, ML, DL ou LLMs | 10.058 |
| └ Correlatos | apenas tecnologias adjacentes (robótica, NLP, big data, automação, visão computacional) ou só sigla "IA" sem co-ocorrência | 2.937 |
| Universo Humanas | Subset onde `NM_GRANDE_AREA_CONHECIMENTO = "CIÊNCIAS HUMANAS"` | 59.976 |
| **Corpus IA-Humanas** | Interseção `corpus IA × grande área Humanas` | **400** |

### I.2. Corpus IA por ano de defesa

| Ano de base | Defesas no campo IA |
|---:|---:|
| 2021 | 2.615 |
| 2022 | 2.997 |
| 2023 | 3.447 |
| 2024 | 3.936 |
| **Total** | **12.995** ✓ |

Crescimento bruto 2021→2024: +50,5%. CAGR aproximado: 14,6% a.a.

### I.3. Corpus IA por grande área (12.995) — com taxa interna

| Grande área | N IA | % do corpus | Universo da grande área | Taxa interna |
|---|---:|---:|---:|---:|
| Ciências Exatas e da Terra | 3.633 | 27,96% | 25.431 | **14,29%** |
| Engenharias | 3.590 | 27,63% | 29.880 | **12,01%** |
| Ciências Sociais Aplicadas | 1.848 | 14,22% | 53.492 | 3,45% |
| Multidisciplinar | 1.632 | 12,56% | 57.231 | 2,85% |
| Ciências Agrárias | 773 | 5,95% | 27.619 | 2,80% |
| Ciências da Saúde | 741 | 5,70% | 55.121 | 1,34% |
| **Ciências Humanas** | **400** | **3,08%** | **59.976** | **0,67%** |
| Ciências Biológicas | 238 | 1,83% | 19.461 | 1,22% |
| Linguística, Letras e Artes | 140 | 1,08% | 21.860 | 0,64% |
| **Soma corpus** | **12.995** ✓ | **100%** | 350.071 | — |

> **Marginalidade em duas leituras:** Humanas é a maior grande área no universo total (17%) mas só 3,08% do corpus IA, e apenas 0,67% das defesas de Humanas tocam o campo — contra 14,29% em Exatas e 12,01% em Engenharias.

### I.4. Corpus IA por grau acadêmico

| Grau | Defesas | % do corpus |
|---|---:|---:|
| Mestrado | 7.153 | 55,04% |
| Doutorado | 3.925 | 30,20% |
| Mestrado Profissional | 1.874 | 14,42% |
| Doutorado Profissional | 43 | 0,33% |
| **Total** | **12.995** ✓ | 100% |

### I.5. Corpus IA por subcampo (multi-label; soma > 100%)

| Subcampo | Defesas | % do corpus |
|---|---:|---:|
| Aprendizado de máquina (ML) | 5.284 | 40,66% |
| Tecnologias correlatas | 4.972 | 38,26% |
| Aprendizado profundo & redes neurais | 4.326 | 33,29% |
| IA em sentido estrito | 3.821 | 29,40% |
| Modelos de linguagem & IA generativa | 506 | 3,89% |

> **Achado:** ML supera IA stricta em volume (5.284 vs 3.821). LLMs é o menor dos cinco (506) após a correção do regex `transformer` — antes da correção, era 876, inflado por falsos positivos de "transformer" no sentido literal (transformador elétrico, "social transformer" em textos não-técnicos).

### I.6. CAPES IA-Humanas (400) — duas taxonomias

A CAPES opera com **duas classificações distintas** que precisam ser declaradas. O `XLSX` traz ambas como colunas (`NM_AREA_CONHECIMENTO` e `NM_AREA_AVALIACAO`). Os números abaixo são lidos diretamente da planilha; em ambas as colunas a soma fecha em 400.

**Por área de conhecimento (NM_AREA_CONHECIMENTO):**

| Área de conhecimento | Defesas | % de IA-Humanas |
|---|---:|---:|
| Educação | 154 | 38,50% |
| Geografia | 64 | 16,00% |
| Psicologia | 56 | 14,00% |
| Ciência Política | 40 | 10,00% |
| Filosofia | 39 | 9,75% |
| Sociologia | 25 | 6,25% |
| História | 12 | 3,00% |
| **Antropologia** | **4** | **1,00%** |
| Teologia | 4 | 1,00% |
| Arqueologia | 2 | 0,50% |
| **Soma** | **400** ✓ | 100% |

**Por área de avaliação (NM_AREA_AVALIACAO — taxonomia administrativa da CAPES):**

| Área de avaliação CAPES | Defesas |
|---|---:|
| Educação | 154 |
| Geografia | 64 |
| Psicologia | 56 |
| Ciência Política e Relações Internacionais | 40 |
| Filosofia | 39 |
| Sociologia | 25 |
| História | 12 |
| **Antropologia / Arqueologia** | **6** |
| Ciências da Religião e Teologia | 4 |
| **Soma** | **400** ✓ |

**Diferenças entre as duas taxonomias:**

| Área de conhecimento | Área de avaliação | Mudança |
|---|---|---|
| Antropologia (4) + Arqueologia (2) | **Antropologia / Arqueologia (6)** | **Agrupamento** (CAPES une as duas no organograma de programas) |
| Ciência Política (40) | Ciência Política e Relações Internacionais (40) | Mesmo número, nome ampliado |
| Teologia (4) | Ciências da Religião e Teologia (4) | Mesmo número, nome ampliado |
| Educação, Geografia, Psicologia, Filosofia, Sociologia, História | (idem) | Nome idêntico |

### I.6.1. Implicação para a tese — Antropologia 4 ou 6?

A tese pode dizer qualquer um dos dois números, **desde que declare o critério**:

- "**4 defesas em Antropologia**, segundo a área de conhecimento (NM_AREA_CONHECIMENTO) da CAPES" → recorte estrito da disciplina antropológica.
- "**6 defesas na área de avaliação Antropologia / Arqueologia**, segundo o organograma administrativo da CAPES (NM_AREA_AVALIACAO)" → recorte institucional, que reflete como os programas de pós-graduação são, de fato, organizados pela agência.

A recomendação para o texto é **declarar ambos**:

> "A área de Antropologia registra **4 defesas sobre IA** em 2021–2024 (área de conhecimento); na taxonomia de avaliação da CAPES, que agrupa Antropologia e Arqueologia em uma única área administrativa, são **6 defesas**. Ambos os recortes apontam para presença muito baixa frente a Educação (154) ou Geografia (64) — a marginalidade do tema na Antropologia brasileira independe do critério taxonômico adotado."

Essa formulação blinda a tese contra a arguição "4 pela área de conhecimento ou 6 pela área de avaliação?", e mostra domínio das duas chaves de classificação.

### I.6.2. Implicação para Teologia e Ciência Política

- **Teologia** mantém 4 defesas em ambas as colunas, mas o nome oficial CAPES (que entrará na tese se o critério for área de avaliação) é **"Ciências da Religião e Teologia"**, não apenas "Teologia".
- **Ciência Política** mantém 40 defesas em ambas as colunas, mas o nome oficial é **"Ciência Política e Relações Internacionais"**. Essa é a denominação que aparece em currículos Lattes, comitês de avaliação e portarias da CAPES.

Decisão recomendada: **na narrativa da tese, usar os nomes da NM_AREA_AVALIACAO** (que são os formalmente reconhecidos pela CAPES), com a especificação entre parênteses quando relevante.

### I.7. CAPES IA-Humanas — top 10 IES e regiões

**Top 10 IES** (de 400):
UnB (29), USP (26), UFRJ (17), UFMG (12), UFC (12), UFRN (11), UNICAMP (10), UFPE (8), UFRGS (8), UFF (8).

**Distribuição regional** (de 400):
Sudeste 183 (45,75%), Sul 84 (21,00%), Nordeste 71 (17,75%), Centro-Oeste 55 (13,75%), Norte 7 (1,75%).

### I.8. Panorama CAPES (12.995) — top 10 IES e top áreas de conhecimento

**Top 10 áreas de conhecimento no corpus IA total** (12.995):

| Área de conhecimento | Defesas |
|---|---:|
| Ciência da Computação | 2.903 |
| Engenharia Elétrica | 1.838 |
| Interdisciplinar | 1.083 |
| Direito | 747 |
| Administração | 554 |
| Engenharia Mecânica | 491 |
| Engenharia de Produção | 400 |
| Agronomia | 347 |
| Medicina | 347 |
| Engenharia Civil | 248 |

**Top 10 IES no corpus IA total** (12.995):

| IES | Defesas |
|---|---:|
| USP | 647 |
| UNICAMP | 486 |
| UnB | 402 |
| UFMG | 401 |
| UFRJ | 376 |
| UFPE | 343 |
| UFSC | 337 |
| UFRGS | 323 |
| UFPR | 273 |
| UFC | 253 |

**Distribuição regional do corpus IA total** (12.995):

| Região | Defesas | % |
|---|---:|---:|
| Sudeste | 6.730 | 51,79% |
| Sul | 2.569 | 19,77% |
| Nordeste | 2.282 | 17,56% |
| Centro-Oeste | 965 | 7,43% |
| Norte | 449 | 3,46% |

### I.9. Fonte dos números

- Universo total: contagem de linhas dos 4 XLSX `dados_capes/2021-2024/br-capes-btd-*.xlsx` (Git LFS).
- Universo por grande área: `dados_capes/capes_2021_2024_universo_por_grande_area.csv` (cache leve gerado pelo `figuras_capes_2021_2024.py` ao percorrer os 4 XLSX uma vez).
- Corpus IA (12.995) e detalhamentos: `dados_capes/capes_2021_2024_ia_auditoria.xlsx`.
- Subset IA-Humanas (400) e detalhamentos: `dados_capes/capes_2021_2024_ia_humanas_completo.xlsx`.

---

## II. SciELO — coleção Brasil 2021–2024 via API ArticleMeta

### II.1. Coortes

| Coorte | Definição | N |
|---|---|---:|
| Universo SciELO bruto | Todos os artigos da coleta API com `from=2021-01-01 & until=2024-12-31`. Filtro from/until opera sobre `processing_date` (data de indexação no SciELO), não sobre `publication_date` | 98.165 |
| **Universo SciELO do recorte** | Universo restrito a `ano de publicação` 2021–2024 (denominador correto da taxa interna) | **90.360** |
| Corpus IA bruto (`scielo_brasil_ia_subcampos_auditoria.xlsx`) | Subset de IA do universo bruto, sem filtro de ano | 659 |
| **Corpus IA recorte estrito** | Subset IA restrito a `ano de publicação` 2021–2024 | **631** |
| └ Foco Central | 502 |
| └ Correlatos | 129 |
| **Human Sciences puro** | Recorte estrito + `subject_areas_periodico` exatamente igual a "Human Sciences" (sem multi-área) | **72** |

> **Nota sobre o filtro temporal da API:** dos 659 artigos brutos, 28 caem fora da janela de publicação. Eles entram no resultado porque a API filtra `processing_date` (indexação), não `publication_date`. Esses 28 são descartados em todas as análises da tese.

### II.2. Decomposição verificada dos 28 stragglers

| Ano de publicação | Artigos | Subtotal |
|---|---:|---|
| 1986 | 1 | |
| 1990 | 1 | |
| 1992 | 1 | |
| 2004 | 1 | |
| 2019 | 2 | |
| 2020 | 17 | **pré-2021: 23** |
| 2025 | 5 | **pós-2024: 5** |
| **Total fora da janela** | **28** ✓ | |

Soma: 23 + 5 = 28; 28 + 631 = 659 ✓.

### II.3. Corpus IA SciELO recorte (631) por ano de publicação

| Ano | Artigos |
|---:|---:|
| 2021 | 107 |
| 2022 | 145 |
| 2023 | 154 |
| 2024 | 225 |
| **Total** | **631** ✓ |

Crescimento bruto 2021→2024: +110%. CAGR aproximado: 28% a.a. (ritmo mais acelerado que o do CAPES, refletindo ciclo editorial mais curto dos periódicos vs ciclo longo das defesas).

### II.4. SciELO recorte 631 — distribuição por subject_area, com taxa interna

| Subject area | N IA | % do corpus | Universo do recorte | Taxa interna |
|---|---:|---:|---:|---:|
| Health Sciences | 200 | 31,70% | 35.704 | 0,56% |
| Agricultural Sciences | 98 | 15,53% | 9.810 | 1,00% |
| Multidisciplinar (*sintética*) | 84 | 13,31% | 10.163 | 0,83% |
| Engineering | 78 | 12,36% | 4.551 | **1,71%** |
| **Human Sciences** | **72** | **11,41%** | **14.806** | **0,49%** |
| Applied Social Sciences | 66 | 10,46% | 6.100 | 1,08% |
| Exact and Earth Sciences | 25 | 3,96% | 2.032 | 1,23% |
| Biological Sciences | 5 | 0,79% | 4.598 | 0,11% |
| Linguistics, Letters and Arts | 3 | 0,48% | 2.596 | 0,12% |
| **Soma** | **631** ✓ | 100% | **90.360** | — |

Taxa SciELO geral: 631/90.360 = 0,70%.

> **Atenção terminológica:** SciELO tem **8 subject_areas canônicas**. "Multidisciplinar" não é uma — é bucket sintético do nosso pipeline para periódicos cujo `subject_areas_periodico` lista mais de uma área. **Não dizer "9 subject_areas" na tese.** Formulação precisa: "as 8 subject_areas do SciELO, mais uma categoria 'Multidisciplinar' para periódicos com classificação múltipla".

> **Atenção ao denominador:** as taxas internas acima usam o universo do recorte estrito 2021–2024 (90.360), NÃO o universo bruto da coleta (98.165). Numerador e denominador são apples-to-apples.

### II.5. SciELO recorte 631 — distribuição por subcampo (multi-label; soma > 100%)

| Subcampo | Artigos | % do corpus |
|---|---:|---:|
| IA em sentido estrito | 187 | 29,64% |
| Aprendizado profundo & redes neurais | 158 | 25,04% |
| Tecnologias correlatas | 140 | 22,19% |
| Aprendizado de máquina (ML) | 138 | 21,87% |
| Modelos de linguagem & IA generativa | 45 | 7,13% |

> **Comparação com CAPES (bloco I.5):** o SciELO inverte a hierarquia. No CAPES, ML lidera (40,66%) e IA stricto é o quarto (29,40%); no SciELO, IA stricto lidera (29,64%) e ML é o quarto (21,87%). Padrão coerente com a tese de que periódicos publicam mais "IA como conceito" e defesas trabalham mais com técnica aplicada.

### II.6. SciELO Human Sciences puro (72) — top 10 periódicos

Subset que vai para o comparativo SciELO × CAPES.

| Periódico | Artigos |
|---|---:|
| Estudos Avançados | 13 |
| Trans/Form/Ação | 9 |
| Filosofia Unisinos | 6 |
| Revista Brasileira de Ensino de Física | 6 |
| Ciência & Educação (Bauru) | 5 |
| Psicologia: Reflexão e Crítica | 3 |
| **Mana** | **3** |
| Educação em Revista | 3 |
| Mercator (Fortaleza) | 2 |
| Revista Brasileira de Inovação | 2 |

> **Achado para a Antropologia:** dos **3 artigos publicados em Mana** (periódico antropológico de referência do PPGAS-MN/UFRJ), **todos são de 2024** e **todos tocam o tema via big data** (subcampo Correlatos), não via IA stricta. Títulos: "Reflexões sobre big data, sexualidades, datificação e moralidades no pornô digital"; "Quem Precisa de Big Data?: sobre dados e informação na agricultura de precisão"; "Big Data: Modos de fazer, comparar e governar". A Antropologia, quando entra na conversa nos periódicos, entra pela porta dos correlatos (não pela IA stricto sensu) e em 2024 (recente). Isso fortalece o argumento da tese sobre a emergência tardia e tematicamente desviada do tema no campo antropológico.

### II.7. Fonte dos números

- Universo bruto e recorte: `dados_scielo/scielo_brasil_ia_subcampos_auditoria.xlsx` (659 linhas brutas, 631 no recorte).
- Universo por subject_area (recorte): `dados_scielo/scielo_brasil_universo_agregado.csv` (90.360 totalizados).
- Cache completo da coleta: `dados_scielo/cache_articlemeta/` (~98k JSONs, gitignored).

---

## III. Comparativo SciELO Human Sciences puro × CAPES Humanas

Único cruzamento direto na tese. Paridade real apples-to-apples: SciELO restrito a `subject_area = "Human Sciences"` puro (sem multi-área) contra CAPES grande área "Ciências Humanas". Tabela completa em `tabelas_comparativas_2026.md`.

| Indicador | SciELO Human Sciences | CAPES Humanas |
|---|---:|---:|
| Total no campo IA/ML/DL | 72 | 400 |
| Foco Central | 52 | 234 |
| Correlatos | 20 | 166 |
| Universo (denominador) | 14.806 | 59.976 |
| **Taxa interna** | **0,49%** | **0,67%** |
| Crescimento 2021→2024 | 16 → 34 (+113%) | 69 → 142 (+106%) |

> **Não confundir** com a taxa SciELO geral (0,70%), que se refere ao universo SciELO total 631/90.360, não ao recorte Human Sciences puro.

---

## IV. OpenAlex — produção internacional de IA nas Humanidades 2016–2024

Terceira fonte, de escopo **internacional**. Coleta via API REST (`analise_openalex.py`), aplicando o **mesmo `utils.classificar_subcampos`** das outras bases. Permite o que CAPES e SciELO não dão: comparação por país e contexto mundial.

### IV.1. Recorte (definição de "Humanidades" no OpenAlex)

O OpenAlex não tem uma área "Ciências Humanas"; tem *fields* (taxonomia Scopus/ASJC). Para espelhar o "Ciências Humanas" da CAPES adotamos o recorte **amplo** `12|32|33`:

| ID | Field OpenAlex | Equivalência CAPES |
|---:|---|---|
| 12 | Arts and Humanities | Filosofia, História, Teologia, Artes |
| 32 | Psychology | Psicologia (a CAPES conta em Humanas; OpenAlex separa) |
| 33 | Social Sciences | Sociologia, Ciência Política, Geografia, Antropologia, Educação |

IDs confirmados em 2026-06-06 via `--listar-campos`. IA = conceito `C154945302` ("Artificial intelligence"). Janela 2016–2024 (alinhada à base OWID/CSET).

### IV.2. Duas definições de "IA" — declarar qual

A MESMA base produz números muito diferentes conforme a definição de IA:

| Definição | Critério | Brasil IA-Humanas |
|---|---|---:|
| **Conceito OpenAlex** | tag algorítmica `C154945302` | **9.996** |
| **Palavra-chave** | `utils.classificar_subcampos` em título+resumo (mesma régua de CAPES/SciELO) | **849** |

> **Achado:** apenas **8,5%** das obras que o OpenAlex marca como IA contêm vocabulário de IA em título/resumo. O número comparável às outras bases do projeto é **849** (palavra-chave), não 9.996. Provável causa do abismo: conceito do OpenAlex generoso + obras sem resumo (régua tem menos texto para casar).

### IV.3. Brasil — coorte palavra-chave por obra única (849)

Contagem por **obra única** (deduplicada por `openalex_id`; a contagem por linha obra×país = 15.438 infla ~54% por coautoria internacional).

| FOCO_IA | Obras únicas |
|---|---:|
| Foco Central | 713 |
| Correlato | 136 |
| **Total que toca IA** | **849** |
| (Outros Temas, do universo-conceito) | 9.147 |

### IV.4. Brasil — subcampos (multi-label; soma > total)

| Subcampo | Obras | % de 849 |
|---|---:|---:|
| IA em sentido estrito | 288 | 33,9% |
| Aprendizado de máquina (ML) | 288 | 33,9% |
| Tecnologias correlatas | 242 | 28,5% |
| Aprendizado profundo & redes neurais | 228 | 26,9% |
| Modelos de linguagem & IA generativa | 56 | 6,6% |

> **Triangulação dos subcampos:** CAPES tem ML > IA stricto; SciELO tem IA stricto > ML; **OpenAlex empata (288 = 288)**. LLM é o menor nas três bases (CAPES 3,89% / SciELO 7,13% / OpenAlex 6,6%).

### IV.5. Contexto internacional (conceito OpenAlex, por país, 2016–2024)

Top por volume de IA-Humanas (definição conceito). Universo = todas as obras de Humanidades do país; taxa interna = IA-Humanas / universo.

| País | IA-Humanas | Universo | Taxa interna |
|---|---:|---:|---:|
| Estados Unidos | ~60.943 | 990.707 | 6,15% |
| China | 51.300 | 303.733 | **16,89%** |
| Reino Unido | 42.823 | 594.599 | 7,20% |
| Alemanha | 27.504 | 419.966 | 6,55% |
| **Brasil** | **9.996** | **636.607** | **1,57%** |

> **Achado para a tese:** o Brasil tem o **2º maior universo de Humanidades** do top mundial (636.607, atrás só dos EUA), mas a **menor taxa interna do top-20 (1,57%)**. Confirma, em escala internacional, a "marginalidade" já vista na CAPES (0,67%): o gargalo brasileiro não é produzir pouco em Humanidades, é o quão pouco dessa produção dialoga com IA. (Nota: 2024 provavelmente subestimado por indexação incompleta no OpenAlex.)

### IV.6. Ressalvas

- **Viés de idioma:** OpenAlex privilegia metadados em inglês → subestima produção em português/chinês (afeta Brasil e China).
- **Contagem por país:** uma obra conta uma vez por país de afiliação (colaboração internacional entra em vários); os números canônicos por obra única do bloco IV.3 deduplicam isso.
- **`primary_topic`** é o tópico principal atribuído por modelo; obras multidisciplinares caem num único *field*.

### IV.7. Fonte dos números

- Por país e por ano (definição conceito): `dados_openalex/openalex_ia_humanas_por_pais_global.csv`, `openalex_ia_humanas_por_ano_BR.csv`.
- Coorte palavra-chave (849) e subcampos: `dados_openalex/openalex_ia_humanas_resumo_BR.csv` e `openalex_ia_humanas_auditoria_BR.xlsx`.
- Corpus completo (regenerável, gitignored): `openalex_ia_humanas_corpus_BR.csv`.

---

## V. Coortes históricas (NÃO usar como fonte para a tese)

Estas coortes foram superadas durante o trabalho. **Persistem no repositório** por reprodutibilidade do processo, **não como evidência válida**.

| Coorte | N | Status |
|---|---:|---|
| SciELO 1983–2025 (coleta web inicial) | 152 | Substituída pela coleta API. |
| SciELO recorte 3 áreas-alvo (coleta intermediária) | 179 (estrito) / 188 (bruto) | Substituída pelo universo Brasil completo 631 e pelo Human Sciences puro 72. |
| CAPES 2013–2023 web inicial | 100 | Substituída pelo dump oficial 2021–2024 = 12.995. |
| CAPES IA total ANTES da correção `transformer` | 13.336 | Substituída por **12.995** (pós-correção do regex). |
| LLM CAPES antes da correção `transformer` | 876 | Substituído por **506**. |
| Health Sciences (SciELO) na coorte bruta 659 | 207 | Na coorte estrita 631: **200**. |
| Human Sciences (SciELO) na coorte bruta 659 | 74 | Na coorte estrita 631: **72**. |
| CAPES Humanas ANTES da correção `transformer` | 441 | Substituída por **400**. |
| Top IES CAPES Humanas antes da correção | UnB 30, USP 27, UFRJ 18 | Após correção: UnB 29, USP 26, UFRJ 17. |
| Sudeste 200 / Sul 96 / NE 79 (CAPES, antes) | — | Após correção: 183 / 84 / 71. |
| Crescimento CAPES 2.716 → 4.020 (coorte 13.336) | — | Coorte atual: **2.615 → 3.936**. |

---

## VI. Como atualizar este arquivo

1. Quando refizer uma coleta ou um recorte, ATUALIZE este arquivo **antes** de mudar o README ou qualquer figura.
2. Para cada número novo, anote a coorte, o XLSX/CSV fonte, e a operação pandas que o produziu.
3. Faça um commit dedicado ("decisoes_metodologicas: atualiza N para Y após verificação de X") — não junte com mudança de figura ou texto.
4. Em seguida, sincronize README, inventário e tabelas para citar deste arquivo.
5. **Regra de método:** todo número desta página sai de operação atômica em pandas (`len`, `value_counts`, `groupby().size()`, divisão direta), nunca de soma feita em prosa.

*Última verificação completa: 23 de maio de 2026 — auditoria cruzada de `capes_2021_2024_ia_auditoria.xlsx`, `capes_2021_2024_ia_humanas_completo.xlsx`, `capes_2021_2024_universo_por_grande_area.csv`, `scielo_brasil_ia_subcampos_auditoria.xlsx` e `scielo_brasil_universo_agregado.csv`. Todos os números foram lidos via pandas diretamente das fontes primárias, não inferidos. Achados narrativos novos propagados para README e inventário no mesmo dia: (a) os 3 artigos de Mana são todos de 2024 e todos via big data (subcampo Correlatos), não IA stricto; (b) inversão da hierarquia de subcampos entre as bases — CAPES tem ML > IA stricto, SciELO tem IA stricto > ML; (c) distinção NM_AREA_CONHECIMENTO (disciplinar) vs NM_AREA_AVALIACAO (administrativa CAPES), que afeta especialmente a contagem de Antropologia (4 vs 6). Auditoria figura-a-figura do inventário no mesmo dia detectou e corrigiu quatro captions com números pré-auditoria: (i) capes_15 "53/35/12%" → "55,0/30,2/14,4%" + Doutorado Profissional 0,3%; (ii) capes_h02 "80 → mais de 150" → "69 → 142 (+106%)"; (iii) scielo_15 "português dominante" → INVERSÃO, inglês domina com 487 (77,2%); (iv) capes_17 top IES com ordem verificada (USP 647, UNICAMP 486, UnB 402, UFMG 401, UFRJ 376, etc.).*

---

## Padronização de cor por base de dados (27 de junho de 2026)

Decisão de visualização: cada base de dados passa a ter uma cor-assinatura única
nos gráficos de barras, em vez de uma cor por subcampo. O leitor identifica a
base pela cor, de modo consistente entre as figuras.

- **CAPES → verde** (`CORES_INTERMEDIARIAS[2]`, `#81C784`)
- **SciELO → azul** (`CORES_INTERMEDIARIAS[3]`, `#64B5F6`)
- **OpenAlex → vermelho** (`CORES_INTERMEDIARIAS[0]`, `#E57373`)

O mapa segue o que `openalex_04_subcampos_3bases` já adotava (única figura em que
as três bases aparecem juntas), agora estendido às distribuições por subcampo.
`capes_21_subcampos_distribuicao` (5 barras, todas verdes) e
`scielo_21_subcampos_distribuicao` (5 barras, todas azuis) deixaram de usar a
paleta de cinco cores por subcampo; `openalex_04` permanece como estava e valida
o esquema. Aplicado em `figuras_capes_2021_2024.py` (fig21) e
`figuras_scielo_articlemeta.py` (fig21). Nenhum número mudou: a recoloração das
figuras já publicadas foi feita sobre o SVG, preservando contagens e layout
(SciELO mantém a coorte estrita N=631).
