# Inventário de figuras — análise CAPES 2021–2024

Documento de apoio para a redação do Capítulo 2 da tese. Para cada figura, contém:

- **Caminho do arquivo** no repositório (`figuras/...`)
- **Bloco LaTeX pronto** com `\caption{...}`, `\label{...}` e `\source{...}` — basta copiar e colar
- **Comentário analítico** com o que destacar no texto que acompanha a figura

Convenções adotadas:

- Todas as figuras vêm do dump oficial CAPES `BR-CAPES-BTD-2021A2024-2025-12-01` (versão 3.0, gerado 24/11/2025), totalizando 350.071 trabalhos de conclusão de pós-graduação stricto sensu, dos quais 12.995 foram identificados no corpus "Tecnologias de IA, ML e aprendizado profundo" pelo classificador refinado.
- **As figuras não trazem título embutido na imagem**: a identificação é feita pelo nome do arquivo e pela `\caption{}` abaixo. Toda figura é gerada em **dois formatos com o mesmo nome-base** — `.png` (raster, 300 dpi, para `\includegraphics`) e `.svg` (vetorial, para edição ou saída vetorial). Os blocos abaixo usam o `.png`; troque a extensão se preferir o `.svg` (requer suporte a SVG no seu fluxo LaTeX, p. ex. `svg`/Inkscape).
- O `\source{...}` usa o comando comum em teses brasileiras; troque por `\fonte{}`, `\floatfoot{}` ou similar conforme o template do PPGAS-USP.
- As `\label{}` seguem o padrão `fig:capes_NN_descritor` para fácil referência via `\autoref{}` ou `\Cref{}`.
- O ambiente assume `\usepackage{graphicx}` e largura padrão `0.95\linewidth` — ajuste conforme o layout.

> **Outras fontes:** este inventário cobre as figuras das fontes **CAPES** e **SciELO**. As figuras da fonte **OpenAlex** (internacional) — 15 figuras `openalex_01`…`openalex_15`, com legendas e discussão prontas — estão no inventário paralelo [`docs/inventario_figuras_openalex.tex`](docs/inventario_figuras_openalex.tex).

---

## Painel geral — corpus completo

### Figura 11 — Distribuição por grande área (absoluto + taxa interna)

`figuras/capes_11_grande_area_share.png`

```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.95\linewidth]{figuras/capes_11_grande_area_share.png}
  \caption{Distribuição dos 12.995 trabalhos sobre Tecnologias de IA, ML e aprendizado profundo defendidos na pós-graduação brasileira (2021--2024) por grande área de conhecimento. O painel esquerdo mostra o volume absoluto e a participação percentual no corpus; o painel direito mostra a taxa interna --- isto é, a fração das defesas da grande área que tratam do campo. Ciências Humanas (destacadas em vermelho) figuram como a maior grande área no universo total (59.976 defesas, 17,1\% do dump), mas representam apenas 3,1\% do corpus IA/ML/DL e 0,7\% das defesas da própria grande área tratam do tema --- contra 14,3\% em Ciências Exatas e 12,0\% em Engenharias.}
  \label{fig:capes_11_grande_area}
  \source{Elaboração própria a partir do Catálogo de Teses e Dissertações da CAPES (BR-CAPES-BTD-2021A2024-2025-12-01).}
\end{figure}
```

**Comentário analítico.** Esta é a figura-síntese da virada metodológica para "todas as áreas". Ela permite que o leitor leia a marginalidade em duas chaves complementares: (i) chave **absoluta** --- Humanas é minoria expressiva no corpus; (ii) chave **relativa** --- mesmo dentro de Humanas, IA é objeto periférico. A diferença com Exatas/Engenharias é de uma ordem de grandeza (14× a 18×). Use como abertura da seção de resultados.

---

### Figura 12 — Evolução temporal por grande área (2021–2024)

`figuras/capes_12_temporal_grande_area.png`

```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.95\linewidth]{figuras/capes_12_temporal_grande_area.png}
  \caption{Evolução anual (2021--2024) do número de defesas sobre Tecnologias de IA, ML e aprendizado profundo por grande área de conhecimento. Cada linha corresponde a uma das nove grandes áreas; Ciências Humanas aparece destacada em vermelho. A inclinação das curvas mostra que o crescimento do campo é generalizado, mas distribuído de forma desigual: Ciências Exatas e Engenharias dominam em volume e ritmo, enquanto Humanas crescem em ritmo proporcional menor.}
  \label{fig:capes_12_temporal_grande_area}
  \source{Elaboração própria a partir do Catálogo de Teses e Dissertações da CAPES (BR-CAPES-BTD-2021A2024-2025-12-01).}
\end{figure}
```

**Comentário analítico.** Usar para mostrar que o ponto da marginalidade não é "Humanas não está crescendo" --- está crescendo --- mas que cresce no mesmo nível baixo, sem fechar o gap com Exatas/Engenharias. A taxa de crescimento composto (CAGR) do corpus total é de cerca de 14\% a.a., similar entre grandes áreas; o que muda é o ponto de partida.

---

### Figura 13 — Heatmap grande área × keyword

`figuras/capes_13_heatmap_area_keyword.png`

```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.95\linewidth]{figuras/capes_13_heatmap_area_keyword.png}
  \caption{Mapa de calor da co-ocorrência entre dez termos-chave do campo das Tecnologias de IA, ML e aprendizado profundo e as nove grandes áreas de conhecimento da CAPES, sobre o corpus de 12.995 defesas. Cada célula reporta o percentual do termo na linha (subcampo) concentrado naquela grande área e, entre parênteses, a contagem absoluta. A leitura por coluna evidencia, por exemplo, que ``redes neurais'' e ``machine/deep learning'' concentram-se em Ciências Exatas e Engenharias, enquanto ``ChatGPT/GPT-N'' aparece distribuído por todas as áreas, com presença particular em Sociais Aplicadas e Humanas.}
  \label{fig:capes_13_heatmap_area_keyword}
  \source{Elaboração própria a partir do Catálogo de Teses e Dissertações da CAPES (BR-CAPES-BTD-2021A2024-2025-12-01).}
\end{figure}
```

**Comentário analítico.** Esta figura revela a **assinatura discursiva** de cada grande área. Humanas conversam com o campo via "IA" e termos correlatos (ChatGPT, IA generativa), mas raramente via termos técnicos (redes neurais, deep learning). Engenharias têm o padrão inverso. Útil para fundamentar a tese de que "IA" significa coisas diferentes em diferentes áreas, mesmo quando a contagem agregada parece uniforme.

> **Ressalva de dados (importante para regerar).** Esta é a única figura cujas **contagens absolutas dependem do resumo** (`DS_RESUMO`): o texto de busca das *keywords* é montado a partir de título + palavras-chave + resumo. A versão canônica usa `dados_capes/capes_2021_2024_ia.csv` (com resumo). Se o script `figuras_capes_2021_2024.py` for rodado apenas com o fallback `capes_2021_2024_ia_auditoria.xlsx` (sem a coluna de resumo), os **valores absolutos caem ~40–50%** (as proporções por área se mantêm), pois muitos *matches* vêm do resumo. As demais figuras CAPES não usam o resumo e não são afetadas. Garanta a presença do `.csv` completo antes de regerar esta figura.

---

### Figura 14 — Evolução total do corpus (Foco Central + Correlatos)

`figuras/capes_14_temporal_total.png`

```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.95\linewidth]{figuras/capes_14_temporal_total.png}
  \caption{Evolução anual do corpus completo (2021--2024) discriminado em Foco Central (presença de termos de IA, ML, DL ou LLMs) e Correlatos (presença apenas de tecnologias adjacentes como robótica, NLP, big data ou visão computacional). O total cresce de 2.615 defesas em 2021 para 3.936 em 2024 (acréscimo de 51\% em quatro anos, CAGR aproximado de 15\% a.a.). O Foco Central representa a maior parte do crescimento; Correlatos mantém-se relativamente estável em volume absoluto.}
  \label{fig:capes_14_temporal_total}
  \source{Elaboração própria a partir do Catálogo de Teses e Dissertações da CAPES (BR-CAPES-BTD-2021A2024-2025-12-01).}
\end{figure}
```

**Comentário analítico.** Substitui a velha métrica de "crescimento 3.000\%" baseada em base muito pequena (2013--2023, 100 trabalhos). O CAGR de 14\% sobre uma base já robusta (2.700+/ano) é uma medida muito mais defensável do crescimento do campo.

---

### Figura 15 — Nível acadêmico

`figuras/capes_15_nivel_academico.png`

```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.85\linewidth]{figuras/capes_15_nivel_academico.png}
  \caption{Distribuição do corpus de 12.995 defesas sobre Tecnologias de IA, ML e aprendizado profundo (2021--2024) por grau acadêmico. O Mestrado responde pela maioria das defesas (7.153, 55,0\%), seguido pelo Doutorado (3.925, 30,2\%) e pelo Mestrado Profissional (1.874, 14,4\%). O Doutorado Profissional, modalidade ainda incipiente, aparece com participação residual (43 defesas, 0,3\%).}
  \label{fig:capes_15_nivel_academico}
  \source{Elaboração própria a partir do Catálogo de Teses e Dissertações da CAPES (BR-CAPES-BTD-2021A2024-2025-12-01).}
\end{figure}
```

**Comentário analítico.** O Mestrado predomina em volume, o que é esperado dada a estrutura do sistema. Mas a presença significativa do Mestrado Profissional sinaliza que a modalidade tem absorvido demanda aplicada do campo.

---

### Figura 16 — Top 20 áreas de conhecimento

`figuras/capes_16_top_areas_conhecimento.png`

```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.85\linewidth]{figuras/capes_16_top_areas_conhecimento.png}
  \caption{Vinte áreas de conhecimento com maior volume de defesas sobre Tecnologias de IA, ML e aprendizado profundo no quadriênio 2021--2024. As barras em vermelho assinalam áreas pertencentes à grande área de Ciências Humanas; as barras em cinza, as demais grandes áreas. A predominância de Ciência da Computação, Engenharia Elétrica e áreas técnicas correlatas é evidente; as áreas de Humanas que aparecem na lista --- Educação à frente --- chegam ao top 20 pela via aplicada, não pela via teórica.}
  \label{fig:capes_16_top_areas_conhecimento}
  \source{Elaboração própria a partir do Catálogo de Teses e Dissertações da CAPES (BR-CAPES-BTD-2021A2024-2025-12-01).}
\end{figure}
```

**Comentário analítico.** Mostra que mesmo em granularidade de área (e não só de grande área), Humanas está sub-representada. Educação aparece no top 20 graças ao volume bruto do campo educacional, mas Antropologia, Sociologia, Filosofia ficam de fora desta lista.

---

### Figura 17 — Top 20 instituições

`figuras/capes_17_top_instituicoes.png`

```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.85\linewidth]{figuras/capes_17_top_instituicoes.png}
  \caption{Vinte instituições de ensino superior com maior volume de defesas sobre Tecnologias de IA, ML e aprendizado profundo no quadriênio 2021--2024. A concentração nas universidades públicas federais e estaduais é expressiva; USP (647 defesas), UNICAMP (486), UnB (402), UFMG (401), UFRJ (376), UFPE (343), UFSC (337), UFRGS (323), UFPR (273) e UFC (253) lideram o ranking.}
  \label{fig:capes_17_top_instituicoes}
  \source{Elaboração própria a partir do Catálogo de Teses e Dissertações da CAPES (BR-CAPES-BTD-2021A2024-2025-12-01).}
\end{figure}
```

**Comentário analítico.** Reforça a centralidade do sistema público de pós-graduação no campo. A ausência de instituições privadas no topo ressoa o argumento da tese sobre a infraestrutura institucional da pesquisa em IA no Brasil.

---

### Figura 18 — Distribuição regional e por UF

`figuras/capes_18_regiao_uf.png`

```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.95\linewidth]{figuras/capes_18_regiao_uf.png}
  \caption{Distribuição geográfica do corpus de defesas sobre Tecnologias de IA, ML e aprendizado profundo (2021--2024). À esquerda, o total por região; à direita, as 15 unidades federativas com maior volume. A concentração no Sudeste (em particular SP, RJ e MG) é a característica dominante, seguida pelo Sul. O eixo Norte permanece marginal --- padrão estrutural da pós-graduação brasileira.}
  \label{fig:capes_18_regiao_uf}
  \source{Elaboração própria a partir do Catálogo de Teses e Dissertações da CAPES (BR-CAPES-BTD-2021A2024-2025-12-01).}
\end{figure}
```

**Comentário analítico.** Documenta a desigualdade regional, que se reproduz quase intacta dentro do campo de IA.

---

### Figura 19 — Distribuição de páginas

`figuras/capes_19_paginas.png`

```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.85\linewidth]{figuras/capes_19_paginas.png}
  \caption{Histograma do número de páginas das defesas do corpus (excluindo casos com menos de 20 ou mais de 800 páginas, prováveis erros de digitação). A linha vermelha marca a mediana. A distribuição é assimétrica à direita: a maior parte das defesas tem entre 80 e 200 páginas, com cauda longa de teses mais volumosas.}
  \label{fig:capes_19_paginas}
  \source{Elaboração própria a partir do Catálogo de Teses e Dissertações da CAPES (BR-CAPES-BTD-2021A2024-2025-12-01).}
\end{figure}
```

**Comentário analítico.** Métrica de apoio. Útil se o capítulo discutir características formais das defesas (tamanho típico, dispersão).

---

### Figura 20 — Top termos em títulos

`figuras/capes_20_top_termos.png`

```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.85\linewidth]{figuras/capes_20_top_termos.png}
  \caption{Vinte e cinco termos mais frequentes nos títulos das 12.995 defesas do corpus, após remoção de stopwords e dos próprios termos canônicos do regex de IA (inteligência, artificial, machine, deep, learning etc.). O ranking revela o entorno semântico do campo --- vocabulários de aplicação (saúde, educação, classificação, predição) e de objetos (dados, sistemas, modelos) --- sem ser dominado pelos termos que definem o filtro.}
  \label{fig:capes_20_top_termos}
  \source{Elaboração própria a partir do Catálogo de Teses e Dissertações da CAPES (BR-CAPES-BTD-2021A2024-2025-12-01).}
\end{figure}
```

**Comentário analítico.** Útil como tabela complementar para discutir o vocabulário aplicado do campo. Considerar se pares ou trios de termos (bigrams) seriam mais informativos do que tokens isolados.

---

## Análise por subcampo

### Figura 21 — Distribuição por subcampo

`figuras/capes_21_subcampos_distribuicao.png`

```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.85\linewidth]{figuras/capes_21_subcampos_distribuicao.png}
  \caption{Distribuição das 12.995 defesas do corpus pelos cinco subcampos do classificador (presença pode ocorrer simultaneamente em múltiplos subcampos). Aprendizado de máquina (ML) é o subcampo mais frequente (5.284 defesas, 40,7\%), seguido por Tecnologias correlatas (38,3\%) e Aprendizado profundo \& redes neurais (33,3\%). IA em sentido estrito vem em quarto lugar (29,4\%), o que contraria a expectativa de que ``IA'' seja o rótulo dominante. Modelos de linguagem \& IA generativa é o menor subcampo em volume (506), mas o que mais cresce em ritmo.}
  \label{fig:capes_21_subcampos_distribuicao}
  \source{Elaboração própria a partir do Catálogo de Teses e Dissertações da CAPES (BR-CAPES-BTD-2021A2024-2025-12-01).}
\end{figure}
```

**Comentário analítico.** Figura central da argumentação contra o uso aglutinador do termo "IA". Sustenta empiricamente a tese de que tratar IA, ML, DL e LLMs como sinônimos mascara hierarquias relevantes do campo brasileiro.

---

### Figura 22 — Heatmap subcampo × grande área

`figuras/capes_22_heatmap_subcampo_grande_area.png`

```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.95\linewidth]{figuras/capes_22_heatmap_subcampo_grande_area.png}
  \caption{Mapa de calor da concentração dos cinco subcampos do classificador entre as nove grandes áreas. Cada linha (subcampo) está normalizada para somar 100\%, mostrando, para cada técnica, onde ela se concentra. Aprendizado profundo e redes neurais concentram-se massivamente em Ciências Exatas e Engenharias; Modelos de linguagem \& IA generativa, em contraste, distribui-se de forma mais espalhada, com presença notável em Sociais Aplicadas, Multidisciplinar e Humanas. Tecnologias correlatas (NLP, big data, robótica, automação) têm distribuição intermediária.}
  \label{fig:capes_22_heatmap_subcampo_grande_area}
  \source{Elaboração própria a partir do Catálogo de Teses e Dissertações da CAPES (BR-CAPES-BTD-2021A2024-2025-12-01).}
\end{figure}
```

**Comentário analítico.** Achado relevante para o argumento da tese: **LLMs/IA generativa é o subcampo que mais atravessa fronteiras**. Quando uma defesa fora das exatas toca o campo, é mais provável que toque por LLMs do que por redes neurais. Isso resoa com a hipótese antropológica sobre o ChatGPT como ponto de virada da entrada da IA no discurso público e humanístico.

---

### Figura 23 — Evolução temporal por subcampo

`figuras/capes_23_temporal_subcampos.png`

```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.95\linewidth]{figuras/capes_23_temporal_subcampos.png}
  \caption{Evolução temporal (2021--2024) das defesas em cada um dos cinco subcampos. Aprendizado de máquina mantém-se como o subcampo de maior volume ao longo de todo o período. Modelos de linguagem \& IA generativa, ainda que seja o menor em volume absoluto, apresenta o crescimento proporcionalmente mais expressivo em 2024 --- corolário da popularização do ChatGPT (lançado em novembro de 2022) e da entrada do tema na pauta pública e acadêmica.}
  \label{fig:capes_23_temporal_subcampos}
  \source{Elaboração própria a partir do Catálogo de Teses e Dissertações da CAPES (BR-CAPES-BTD-2021A2024-2025-12-01).}
\end{figure}
```

**Comentário analítico.** Documenta a "virada generativa" de 2024 com dados oficiais. O salto de LLMs/Generativa é proporcionalmente o maior --- ainda que em base baixa --- e marca o momento em que o campo da IA generativa começa a ser absorvido pela pós-graduação brasileira.

---

## Zoom em Ciências Humanas

### Figura H01 — Áreas de conhecimento em IA-Humanas

`figuras/capes_h01_areas_humanas.png`

```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.85\linewidth]{figuras/capes_h01_areas_humanas.png}
  \caption{Distribuição das 400 defesas no campo das Tecnologias de IA, ML e aprendizado profundo dentro da grande área de Ciências Humanas (2021--2024), por área de conhecimento. Educação responde por 38,5\% das defesas em IA/Humanas; Geografia (16,0\%), Psicologia (14,0\%), Ciência Política (10,0\%) e Filosofia (9,8\%) compõem o segundo bloco. A Antropologia, em destaque, aparece com quatro defesas (1,0\% do total), evidenciando posição marginal dentro do já marginal recorte de Humanas.}
  \label{fig:capes_h01_areas_humanas}
  \source{Elaboração própria a partir do Catálogo de Teses e Dissertações da CAPES (BR-CAPES-BTD-2021A2024-2025-12-01).}
\end{figure}
```

**Comentário analítico.** Figura central da argumentação da tese. A leitura é em duas camadas: dentro de Humanas, IA é um nicho (0,7\% das defesas) --- e dentro desse nicho, a Antropologia é marginal (1\% de um nicho). A marginalidade da Antropologia é, portanto, **dupla**.

---

### Figura H02 — Evolução temporal IA-Humanas por nível

`figuras/capes_h02_temporal_humanas.png`

```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.95\linewidth]{figuras/capes_h02_temporal_humanas.png}
  \caption{Evolução anual (2021--2024) das defesas em Ciências Humanas no campo das Tecnologias de IA, ML e aprendizado profundo, empilhadas por grau acadêmico (Mestrado, Doutorado, Mestrado Profissional). O crescimento é consistente, de 69 defesas em 2021 para 142 em 2024 --- pouco mais que o dobro (+106\%), em ritmo proporcionalmente próximo ao do corpus CAPES total no mesmo período (+51\%). O Mestrado responde pela maior parte do crescimento.}
  \label{fig:capes_h02_temporal_humanas}
  \source{Elaboração própria a partir do Catálogo de Teses e Dissertações da CAPES (BR-CAPES-BTD-2021A2024-2025-12-01).}
\end{figure}
```

**Comentário analítico.** Mostra que as Humanas estão se aproximando do tema --- mas a partir de uma base muito pequena. Importante para nuançar o argumento da marginalidade: ele descreve o estado presente, não uma tendência estática.

---

### Figura H03 — Top 15 IES em IA-Humanas

`figuras/capes_h03_top_ies_humanas.png`

```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.85\linewidth]{figuras/capes_h03_top_ies_humanas.png}
  \caption{Quinze instituições de ensino superior com maior volume de defesas sobre Tecnologias de IA, ML e aprendizado profundo em Ciências Humanas (2021--2024). UnB, USP e UFRJ lideram o conjunto; a presença simultânea de instituições do Sudeste (USP, UFRJ, UFMG, UNICAMP), do Sul (UFRGS) e do Nordeste (UFRN, UFC, UFPE) sugere algum descentramento regional, embora o eixo Sudeste-Sul ainda predomine.}
  \label{fig:capes_h03_top_ies_humanas}
  \source{Elaboração própria a partir do Catálogo de Teses e Dissertações da CAPES (BR-CAPES-BTD-2021A2024-2025-12-01).}
\end{figure}
```

**Comentário analítico.** A USP, instituição da pesquisadora, aparece em segundo lugar (26 defesas, após UnB com 29), o que situa esta tese dentro do contexto institucional onde o tema ganhou tração nas Humanas.

---

### Figura H04 — Distribuição regional IA-Humanas

`figuras/capes_h04_regiao_humanas.png`

```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.75\linewidth]{figuras/capes_h04_regiao_humanas.png}
  \caption{Distribuição regional das defesas em Ciências Humanas no campo das Tecnologias de IA, ML e aprendizado profundo (2021--2024). O Sudeste concentra cerca de 45\% das defesas (em particular SP e RJ); o Sul (UFRGS, UFPR) e o Nordeste (UFC, UFRN, UFPE) compõem a maior parte do restante. O Norte aparece com presença residual.}
  \label{fig:capes_h04_regiao_humanas}
  \source{Elaboração própria a partir do Catálogo de Teses e Dissertações da CAPES (BR-CAPES-BTD-2021A2024-2025-12-01).}
\end{figure}
```

**Comentário analítico.** O recorte de Humanas reproduz, com pequenas variações, a desigualdade regional do conjunto do dump (Figura 18).

---

### Figura H05 — Top termos em IA-Humanas

`figuras/capes_h05_top_termos_humanas.png`

```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.85\linewidth]{figuras/capes_h05_top_termos_humanas.png}
  \caption{Vinte e cinco termos mais frequentes nos títulos das 400 defesas sobre Tecnologias de IA, ML e aprendizado profundo em Ciências Humanas (2021--2024), após remoção de stopwords e dos termos canônicos do regex de IA. O ranking revela o vocabulário próprio do recorte: termos como ``ensino'', ``educação'', ``ética'', ``trabalho'', ``escola'' e ``política'' indicam que a leitura humanística sobre IA aplica-se primariamente a contextos institucionais (escola, mercado de trabalho, política pública) e a problemas normativos (ética, regulação).}
  \label{fig:capes_h05_top_termos_humanas}
  \source{Elaboração própria a partir do Catálogo de Teses e Dissertações da CAPES (BR-CAPES-BTD-2021A2024-2025-12-01).}
\end{figure}
```

**Comentário analítico.** A diferença de vocabulário entre IA-Humanas (educação, ética, trabalho) e o corpus completo (sistemas, dados, predição --- ver Fig. 20) é uma evidência adicional da assinatura discursiva distinta das Humanas no campo.

---

## Painel SciELO 2021–2024 (paralelo ao painel CAPES)

Conjunto de figuras dedicado à análise SciELO via API ArticleMeta, com mesma estrutura analítica do painel CAPES. Universo bruto da coleta API: **98.165 artigos**; universo restrito a 2021–2024 estrito por ano de publicação (denominador correto da taxa interna): **90.360 artigos**. Corpus IA/ML/DL no recorte estrito: **631 artigos** (502 Foco Central + 129 Correlatos; taxa interna geral 631/90.360 = 0,70\%). Nas tabelas, periódicos com múltiplas \textit{subject\_areas} aparecem agrupados na categoria sintética "Multidisciplinar" (não-oficial), resultando em 9 linhas: as 8 áreas SciELO + Multidisciplinar.

### Figura SciELO 11 — Distribuição por subject_area (volume + taxa interna)

`figuras/scielo_11_subject_area_share.png`

```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.95\linewidth]{figuras/scielo_11_subject_area_share.png}
  \caption{Distribuição dos 631 artigos sobre Tecnologias de IA, ML e aprendizado profundo publicados em periódicos da coleção brasileira do SciELO (2021--2024, recorte estrito) pela \textit{subject\_area} primária do periódico. O painel esquerdo mostra o volume absoluto e o percentual no corpus; o painel direito mostra a taxa interna --- isto é, a fração dos artigos da subject\_area que tratam do campo. Health Sciences lidera em volume (200 artigos, 31,7\% do corpus), enquanto Engineering registra a maior taxa interna (1,71\%). Human Sciences, em destaque vermelho, responde por 72 artigos (11,4\% do corpus) com taxa interna de 0,49\% --- magnitude próxima do que CAPES Humanas registra (0,67\%), confirmação independente da marginalidade.}
  \label{fig:scielo_11_subject_area}
  \source{Elaboração própria a partir da API ArticleMeta da SciELO (\textit{articlemeta.scielo.org}, coleção \textit{scl}).}
\end{figure}
```

**Comentário analítico.** Paralelo a Fig. 11 do painel CAPES. **Achado-chave:** Saúde lidera SciELO IA em volume absoluto (200), invertendo a ordem do CAPES (onde Engenharias 28\% e Exatas 27\% dominam). Engenharia mantém a maior taxa interna em ambas as bases. Human Sciences confirma o padrão de marginalidade já visto no CAPES, agora com denominador independente.

---

### Figura SciELO 12 — Evolução temporal por subject_area

`figuras/scielo_12_temporal_subject_area.png`

```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.95\linewidth]{figuras/scielo_12_temporal_subject_area.png}
  \caption{Evolução anual (2021--2024) dos 631 artigos sobre Tecnologias de IA, ML e aprendizado profundo no SciELO Brasil, segmentada pela \textit{subject\_area} primária do periódico. Crescimento agregado de 107 artigos em 2021 para 225 em 2024 (+110\%). Saúde lidera o crescimento em volume absoluto; Human Sciences (em vermelho) acompanha o movimento em ritmo proporcionalmente menor.}
  \label{fig:scielo_12_temporal_subject_area}
  \source{Elaboração própria a partir da API ArticleMeta da SciELO.}
\end{figure}
```

---

### Figura SciELO 13 — Heatmap subject_area × keyword

`figuras/scielo_13_heatmap_sa_keyword.png`

```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.95\linewidth]{figuras/scielo_13_heatmap_sa_keyword.png}
  \caption{Mapa de calor da co-ocorrência entre dez termos-chave do campo e as \textit{subject\_areas} dos periódicos SciELO no recorte estrito 2021--2024 (universo Brasil completo). Cada célula apresenta o percentual da coluna (termo) concentrado naquela linha (área), com contagem absoluta entre parênteses. ``Redes neurais'' e ``machine/deep learning'' concentram-se em Health Sciences, Engineering e Agricultural Sciences; ``ChatGPT/GPT-N'' e ``IA generativa'' aparecem mais distribuídos, com presença proporcionalmente maior em Human Sciences e Applied Social Sciences.}
  \label{fig:scielo_13_heatmap_sa_keyword}
  \source{Elaboração própria a partir da API ArticleMeta da SciELO.}
\end{figure}
```

---

### Figura SciELO 14 — Evolução total (Foco Central + Correlatos)

`figuras/scielo_14_temporal_total.png`

```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.95\linewidth]{figuras/scielo_14_temporal_total.png}
  \caption{Evolução anual (2021--2024) do corpus SciELO Brasil completo, discriminado em Foco Central (artigos que mencionam IA, ML, DL ou LLMs) e Correlatos (apenas tecnologias adjacentes). O total cresce de 107 artigos em 2021 para 225 em 2024 (+110\%), CAGR aproximado de 28\% a.a. --- compatível com o ritmo observado em CAPES Humanas (+106\%).}
  \label{fig:scielo_14_temporal_total}
  \source{Elaboração própria a partir da API ArticleMeta da SciELO.}
\end{figure}
```

---

### Figura SciELO 15 — Idioma dos artigos

`figuras/scielo_15_idioma.png`

```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.85\linewidth]{figuras/scielo_15_idioma.png}
  \caption{Distribuição dos 631 artigos do corpus SciELO Brasil sobre Tecnologias de IA, ML e aprendizado profundo (2021--2024) pelo idioma de publicação. O \textbf{inglês predomina} (487 artigos, 77,2\%), seguido pelo português (127 artigos, 20,1\%) e pelo espanhol (17 artigos, 2,7\%). Padrão coerente com o peso das áreas mais internacionalizadas no recorte expandido (Health Sciences, Engineering, Agricultural Sciences), onde o inglês é o idioma editorial dominante mesmo nos periódicos da coleção brasileira do SciELO. A predominância do inglês é uma inversão do padrão tipicamente lusófono que aparece quando o recorte é restrito a Human Sciences puro.}
  \label{fig:scielo_15_idioma}
  \source{Elaboração própria a partir da API ArticleMeta da SciELO.}
\end{figure}
```

**Comentário analítico.** Paralelo (com adaptação) à Fig. 15 do painel CAPES (que usa nível acadêmico). Aqui usamos idioma como variável de distribuição, dado que SciELO indexa artigos --- não há nível acadêmico associado.

---

### Figura SciELO 16 — Top 20 periódicos

`figuras/scielo_16_top_periodicos.png`

```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.95\linewidth]{figuras/scielo_16_top_periodicos.png}
  \caption{Vinte periódicos do SciELO Brasil com maior volume de artigos sobre Tecnologias de IA, ML e aprendizado profundo no período 2021--2024. Barras em vermelho indicam periódicos cuja \textit{subject\_area} primária é Human Sciences; em cinza, as demais áreas. Com o universo Brasil completo, o ranking passa a refletir o protagonismo de periódicos de Saúde, Engenharia e Multidisciplinares (Anais da ABC); revistas humanísticas como Estudos Avançados, Trans/Form/Ação, Texto Livre, Filosofia Unisinos e Ciência \& Educação permanecem como núcleos do tema dentro de Human Sciences.}
  \label{fig:scielo_16_top_periodicos}
  \source{Elaboração própria a partir da API ArticleMeta da SciELO.}
\end{figure}
```

---

### Figura SciELO 20 — Top termos em títulos

`figuras/scielo_20_top_termos.png`

```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.85\linewidth]{figuras/scielo_20_top_termos.png}
  \caption{Vinte e cinco termos mais frequentes nos títulos dos 631 artigos do corpus SciELO Brasil sobre IA/ML/DL (2021--2024), após remoção de stopwords e dos termos canônicos do regex. O ranking revela o vocabulário de entorno do campo --- termos de aplicação clínica (saúde, diagnóstico, pacientes), técnica (predição, classificação, modelos) e contextuais (sistemas, dados, brasileiros) --- agora ponderado pelo peso de Saúde e Engenharia no corpus expandido.}
  \label{fig:scielo_20_top_termos}
  \source{Elaboração própria a partir da API ArticleMeta da SciELO.}
\end{figure}
```

---

### Figura SciELO 21 — Distribuição por subcampo

`figuras/scielo_21_subcampos_distribuicao.png`

```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.85\linewidth]{figuras/scielo_21_subcampos_distribuicao.png}
  \caption{Distribuição dos 631 artigos do corpus SciELO Brasil pelos cinco subcampos do classificador (presença pode ocorrer simultaneamente em múltiplos subcampos). IA em sentido estrito mantém-se como subcampo dominante (187 artigos, 29,6\%), mas sua hegemonia é mais modesta no universo expandido --- Aprendizado profundo \& redes neurais (158, 25,0\%) e Aprendizado de máquina (138, 21,9\%) seguem de perto. Tecnologias correlatas e Modelos de linguagem \& IA generativa completam o quadro com 22,2\% e 7,1\%, respectivamente.}
  \label{fig:scielo_21_subcampos_distribuicao_scielo}
  \source{Elaboração própria a partir da API ArticleMeta da SciELO.}
\end{figure}
```

**Comentário analítico.** Paralelo à Fig. 21 do painel CAPES. **Inversão de hierarquia entre as duas bases:** no CAPES, ML lidera (40,7\%) e IA em sentido estrito é o quarto subcampo (29,4\%); no SciELO Brasil completo, IA em sentido estrito lidera (29,6\%) e ML é o quarto (21,9\%). A inversão se mantém mesmo com Saúde e Engenharia incluídas no recorte SciELO. Sustenta o argumento sobre a distinção entre escrita periódica (mais "IA como conceito") e escrita de pós-graduação (mais "técnica aplicada").

---

### Figura SciELO 22 — Heatmap subcampo × subject_area

`figuras/scielo_22_heatmap_subcampo_sa.png`

```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.95\linewidth]{figuras/scielo_22_heatmap_subcampo_sa.png}
  \caption{Mapa de calor da concentração dos cinco subcampos do classificador entre as \textit{subject\_areas} dos periódicos SciELO Brasil. Cada linha (subcampo) está normalizada para somar 100\%. Aprendizado profundo \& redes neurais e Aprendizado de máquina concentram-se em Health Sciences, Engineering e Agricultural Sciences; Modelos de linguagem \& IA generativa aparece mais distribuído entre as áreas, com presença proporcional notável em Human Sciences e Applied Social Sciences --- evidência da entrada do tema na pauta humanística pós-ChatGPT.}
  \label{fig:scielo_22_heatmap_subcampo_sa}
  \source{Elaboração própria a partir da API ArticleMeta da SciELO.}
\end{figure}
```

---

### Figura SciELO 23 — Evolução temporal por subcampo

`figuras/scielo_23_temporal_subcampos.png`

```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.95\linewidth]{figuras/scielo_23_temporal_subcampos.png}
  \caption{Evolução temporal (2021--2024) dos cinco subcampos no corpus SciELO Brasil completo. IA em sentido estrito mantém-se na liderança ao longo do período; Aprendizado de máquina e Aprendizado profundo crescem em ritmo expressivo; Modelos de linguagem \& IA generativa, ausente em 2021, dispara em 2024 --- captura empírica direta do impacto da popularização do ChatGPT (lançado novembro/2022) sobre a produção científica brasileira em todas as áreas.}
  \label{fig:scielo_23_temporal_subcampos}
  \source{Elaboração própria a partir da API ArticleMeta da SciELO.}
\end{figure}
```

---

## Comparativo SciELO × CAPES Humanas

### Figura Comparativa — Síntese SciELO × CAPES (2021–2024)

`figuras/comparativo_scielo_capes_2026.png`

```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.98\linewidth]{figuras/comparativo_scielo_capes_2026.png}
  \caption{Análise comparativa SciELO $\times$ CAPES (Ciências Humanas) sobre o quadriênio 2021--2024, com classificador uniforme de subcampos aplicado às duas bases e paridade real de escopo: SciELO restrito ao subset puro de Human Sciences (excluindo multidisciplinares e Applied Social Sciences) contra CAPES grande área Ciências Humanas. (A)~Evolução temporal sobreposta: SciELO Human Sciences cresce de 16 para 34 artigos sobre IA, ML e aprendizado profundo (+113\%); CAPES Humanas cresce de 69 para 142 defesas (+106\%). (B)~Distribuição por subcampo lado a lado: o SciELO Human Sciences é mais conceitual (56\% via ``IA em sentido estrito''), enquanto o CAPES Humanas é mais aplicado (50\% via tecnologias correlatas, sobretudo via Educação). (C)~Top dez periódicos do SciELO Human Sciences no campo, com destaque para Estudos Avançados (13), Trans/Form/Ação (9), Filosofia Unisinos (6), Revista Brasileira de Ensino de Física (6), Ciência \& Educação (5) e a revista de antropologia Mana (3). (D)~Top dez áreas de conhecimento das defesas CAPES em IA/Humanas: Educação (154), Geografia (64), Psicologia (56), Ciência Política (40), Filosofia (39), Sociologia (25), História (12), e a Antropologia com apenas quatro defesas.}
  \label{fig:comparativo_scielo_capes_2026}
  \source{Elaboração própria. Bases: API ArticleMeta (\textit{articlemeta.scielo.org}, coleção \textit{scl}, 72 artigos com \textit{subject\_area} ``Human Sciences'' puro, de um universo de 14.806 artigos dessa área no período) e Catálogo de Teses e Dissertações da CAPES (BR-CAPES-BTD-2021A2024-2025-12-01, 400 defesas da grande área Ciências Humanas, de um universo de 59.976).}
\end{figure}
```

**Comentário analítico.** Figura-síntese que fecha o capítulo. Apresenta as duas bases lado a lado, com metodologia idêntica, sustentando os achados centrais: (i) crescimento expressivo do tema nas humanidades brasileiras; (ii) padrões discursivos distintos entre periódicos (mais conceituais) e teses/dissertações (mais aplicadas); (iii) marginalidade persistente da Antropologia na produção pós-graduada brasileira sobre IA. **Observação qualitativa sobre Mana** (painel C): os 3 artigos da revista são todos de 2024 e todos abordam o tema via *big data*, não via IA stricto sensu — sinal de que a Antropologia entra na conversa tarde e tematicamente desviada, fato que deve ser comentado no texto que acompanha a figura.

---

## Cheat-sheet para referência cruzada no texto

| Argumento da tese | Figura(s) de apoio |
|---|---|
| Marginalidade das Humanas no campo de IA (em volume e em taxa interna) | Fig. 11, Fig. 16 |
| Marginalidade dupla da Antropologia (Humanas é margem, Antro é margem da margem) | Fig. H01, Comp |
| Crescimento do campo sem fechamento do gap | Fig. 12, Fig. 14, Fig. H02, Comp (painel A) |
| Assinatura discursiva: Humanas usam "IA" e correlatos, não "redes neurais" | Fig. 13, Fig. 22, Comp (painel B) |
| ML supera "IA" no Brasil --- crítica ao uso aglutinador do termo | Fig. 21 |
| Virada generativa em 2024 | Fig. 23, Comp (painel A) |
| Concentração institucional e regional | Fig. 17, Fig. 18, Fig. H03, Fig. H04 |
| Vocabulário aplicado das Humanas (educação, ética, trabalho) | Fig. H05 |
| Comparativo SciELO $\times$ CAPES com metodologia uniforme (síntese de fechamento) | Comp |

---

## Bloco LaTeX de definição auxiliar (opcional, no preâmbulo)

Se o seu template ainda não tem o comando `\source`, ele pode ser definido assim:

```latex
\usepackage{caption}
\newcommand{\source}[1]{\caption*{\hfill\footnotesize\textit{Fonte:} #1}}
```

Ou, para uma versão que aparece logo abaixo da caption normal:

```latex
\newcommand{\source}[1]{\par\medskip\noindent\hfill\footnotesize\textit{Fonte:} #1}
```

---

*Documento gerado em 21 de maio de 2026, junto ao branch `claude/analyze-capes-catalog-dEzme` do repositório.*
