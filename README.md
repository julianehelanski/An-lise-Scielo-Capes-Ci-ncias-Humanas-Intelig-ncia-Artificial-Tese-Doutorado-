# Análise Bibliométrica: Inteligência Artificial na Produção Científica Brasileira em Ciências Humanas

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Contributions](https://img.shields.io/badge/Contributions-Welcome-orange.svg)](CONTRIBUTING.md)

## Sobre o Projeto

Este repositório contém dois scripts Python desenvolvidos para análise bibliométrica automatizada de publicações científicas sobre **Inteligência Artificial** na área de **Ciências Humanas** no contexto brasileiro. Os scripts processam dados do **SciELO** e do **Catálogo de Teses da CAPES**, gerando visualizações e relatórios detalhados.

### Objetivos

- **Mapear** a produção científica sobre IA em periódicos brasileiros (SciELO)
- **Analisar** teses e dissertações sobre IA defendidas em universidades brasileiras (CAPES)
- **Identificar** tendências temporais, áreas temáticas e instituições líderes
- **Classificar** automaticamente o foco em IA (central, relacionado ou tangencial)
- **Gerar** visualizações para análise e apresentação

---

## Estrutura do Repositório

```
├── analise_scielo_ia_julianehelanski.py     # Análise de artigos SciELO
├── analise_teses_ia_julianehelanski.py      # Análise de teses CAPES
├── README.md                                 # Este arquivo
├── requirements.txt                          # Dependências
└── exemplos/                                 # Exemplos de outputs
    ├── graficos/
    └── relatorios/
```

---

## Script 1: Análise SciELO (analise_scielo_ia_julianehelanski.py)

### Descrição
Realiza análise integrada de artigos científicos sobre Inteligência Artificial indexados no SciELO, combinando dados de arquivo RIS (exportado da base) com múltiplos arquivos CSV contendo métricas bibliométricas.

### Funcionalidades Principais

#### Processamento de Dados
- **Leitura de arquivo RIS**: Extrai metadados (título, resumo, palavras-chave, ano, periódico, idioma)
- **Integração de CSVs**: Combina dados de:
  - Áreas temáticas (Web of Science)
  - Índices de citação
  - Tipo de literatura (artigos, revisões, editoriais)
  - Documentos citáveis vs. não citáveis
  - Distribuição por periódicos
  - Publicações por ano

#### Classificação Automática por Foco em IA
Sistema de classificação em três níveis:
- **Foco Central em IA**: IA no título ou palavras-chave principais
- **Foco Relacionado**: Menções secundárias ou contextuais
- **Sem Relação**: Não menciona IA

Palavras-chave analisadas incluem: inteligência artificial, machine learning, deep learning, redes neurais, ChatGPT, algoritmos, automação, etc.

#### Categorização Temática
Os artigos com foco em IA são automaticamente categorizados em:
- **Saúde e Medicina**
- **Educação**
- **Direito e Ética**
- **Tecnologia e Computação**
- **Ciências Sociais**
- **Economia e Negócios**
- **Ciências Exatas**
- **Ciências Biológicas**
- **Engenharia**
- **Ciências Ambientais**
- **Artes e Humanidades**

#### Visualizações Geradas (11 gráficos PNG)
1. **Classificação por foco em IA** - Distribuição entre foco central, relacionado e outros
2. **Publicações por ano** - Evolução temporal (dados RIS + CSV)
3. **Top 10 periódicos** - Principais revistas
4. **Outros periódicos** - Distribuição fora do Top 10
5. **Distribuição por idioma** - Português, inglês, espanhol
6. **Tipo de literatura** - Artigos, revisões, etc.
7. **Citável vs. não citável** - Análise de citabilidade
8. **Índices de citação** - Distribuição WoS
9. **Top 10 áreas temáticas** - Principais campos do conhecimento
10. **Outras áreas temáticas** - Áreas fora do Top 10
11. **Categorias temáticas (foco IA)** - Distribuição dos artigos com foco central

#### Relatório Gerado
- **Arquivo TXT** com estatísticas detalhadas, listagem completa de artigos por categoria e ranking de periódicos/áreas

### Entrada de Dados
```
📂 Arquivos necessários (pasta Downloads):
├── export_scielo.ris                    # Exportação SciELO
├── scielo_areas_tematicas.csv           # Áreas WoS
├── scielo_citavel_naocitavel.csv        # Citabilidade
├── scielo_indice_citacoes.csv           # Índices citação
├── scielo_periódicos.csv                # Periódicos
├── scielo_publi_ano.csv                 # Ano publicação
└── scielo_tipo__literatura.csv          # Tipo documento
```

### Saída
```
📁 resultados_analise/
├── 01_foco_ia_classificacao.png
├── 02_publicacoes_por_ano.png
├── ... (11 gráficos totais)
└── relatorio_completo.txt
```

---

## Script 2: Análise CAPES (analise_teses_ia_julianehelanski.py)

### Descrição
Analisa teses e dissertações sobre Inteligência Artificial do Catálogo de Teses e Dissertações da CAPES, gerando visualizações para publicação acadêmica.

### Funcionalidades Principais

#### Análises Realizadas
1. **Classificação por Foco em IA**
   - Foco Central: IA no título
   - Foco Relacionado: termos correlatos (robótica, transhumanismo, automação)
   - Outros Temas: sem relação com IA

2. **Análise Temporal**
   - Evolução das publicações (2013-2023)
   - Cálculo de crescimento percentual
   - Concentração em anos recentes

3. **Nível Acadêmico**
   - Distribuição Mestrado vs. Doutorado
   - Razão M/D
   - Evolução temporal por nível

4. **Análise Institucional**
   - Top 10 instituições produtoras
   - Tipo de instituição (Federal, Estadual, Particular)
   - Distribuição geográfica

5. **Análise de Áreas do Conhecimento**
   - Top 10 áreas temáticas
   - Evolução das top 3 áreas
   - Mapeamento de áreas emergentes

6. **Análise de Palavras-chave**
   - Extração e contagem de termos frequentes
   - Identificação de tendências temáticas

7. **Análise Metodológica**
   - Distribuição do número de páginas
   - Comparação Mestrado vs. Doutorado
   - Estatísticas descritivas

#### Visualizações Geradas (9 gráficos PNG - 300 DPI)
1. **Distribuição Temporal** - Publicações por ano
2. **Foco em IA** - Classificação em 3 níveis
3. **Nível Acadêmico** - Mestrado vs. Doutorado
4. **Top 10 Áreas** - Principais áreas do conhecimento
5. **Evolução M/D** - Tendência temporal por nível
6. **Top 10 Instituições** - Principais universidades
7. **Distribuição de Páginas** - Histograma com estatísticas
8. **Tipo de Instituição** - Federal, Estadual, Particular
9. **Evolução Top 3 Áreas** - Tendência temporal das áreas líderes

#### Exportação de Dados
**Arquivo Excel** com 8 abas:
- Resumo Geral
- Publicações por Ano
- Top 10 Áreas
- Top 10 Instituições
- Foco em IA
- Outras Áreas
- Top Termos
- Dataset Completo

### Entrada de Dados
```
📂 Arquivo necessário (mesma pasta do script):
└── catalogo_teses_analise.xlsx         # Dados CAPES
```

### Saída
```
📁 graficos/
├── 01_distribuicao_temporal.png
├── 02_foco_ia.png
├── ... (9 gráficos totais)
│
└── resultados_detalhados_teses_ia.xlsx  # Excel com 8 abas
```

---

## Como Usar

### Pré-requisitos
```bash
Python 3.8+
```

### Instalação

1. **Clone o repositório**
```bash
git clone https://github.com/seu-usuario/analise-ia-cientifica-brasil.git
cd analise-ia-cientifica-brasil
```

2. **Instale as dependências**
```bash
pip install -r requirements.txt
```

### Dependências
```python
# Análise SciELO
- matplotlib
- seaborn
- numpy
- (bibliotecas padrão: re, os, csv, collections)

# Análise CAPES
- pandas
- numpy
- matplotlib
- seaborn
- openpyxl
```

### Execução

#### Script SciELO
```bash
python analise_scielo_ia_julianehelanski.py
```
**Nota**: Ajuste o caminho `BASE_DIR` no script para o local dos seus arquivos de entrada.

#### Script CAPES
```bash
python analise_teses_ia_julianehelanski.py
```
**Nota**: Certifique-se de que `catalogo_teses_analise.xlsx` está na mesma pasta do script.

---

## Exemplos de Resultados

### Estatísticas Típicas (SciELO)
- Total de artigos analisados: ~100-1000
- Artigos com foco central em IA: 20-40%
- Artigos que mencionam IA: 60-80%
- Principais áreas: Ciência da Computação, Saúde, Educação

### Estatísticas Típicas (CAPES)
- Teses/dissertações: 100 registros (amostra)
- Período: 2013-2023
- Crescimento: ~300-500% na década
- Concentração últimos 3 anos: ~40-50%
- Top área: EDUCAÇÃO (frequentemente)

---

## Personalização

### Adicionar Novas Categorias Temáticas (SciELO)
Edite a função `categorizar_artigo()`:
```python
def categorizar_artigo(artigo):
    # Adicione novos padrões de categoria
    if re.search(r'sua_palavra_chave', texto, re.IGNORECASE):
        return 'Nova Categoria'
```

### Ajustar Classificação de Foco (CAPES)
Modifique as listas de keywords:
```python
keywords_ia_forte = [
    'inteligência artificial',
    'seu_termo_personalizado',
    # ...
]
```

### Customizar Gráficos
Ajuste as configurações visuais:
```python
plt.rcParams['figure.figsize'] = (14, 8)  # Tamanho
plt.rcParams['font.size'] = 12            # Fonte
sns.set_palette("sua_paleta")             # Cores
```

---

## Estrutura dos Dados

### Formato RIS (SciELO)
```
TY  - JOUR
TI  - Título do artigo
AU  - Autor
PY  - 2023
JO  - Nome do periódico
AB  - Resumo
KW  - Palavra-chave
LA  - pt
ER  -
```

### Formato Excel (CAPES)
Colunas necessárias:
- `id`: Identificador
- `titulo`: Título da tese/dissertação
- `autor`: Nome do autor
- `ano_defesa`: Ano
- `nivel`: Mestrado/Doutorado
- `area`: Área do conhecimento
- `instituicao`: Nome da universidade
- `tipo`: Federal/Estadual/Particular
- `num_paginas`: Número de páginas

---

## Características dos Gráficos

- **Alta resolução**: 300 DPI (qualidade de publicação)
- **Fundo branco**: Adequado para artigos acadêmicos
- **Títulos informativos**: Com totais e percentuais
- **Cores profissionais**: Paletas otimizadas para daltonismo
- **Formato PNG**: Compatível com todas as plataformas
- **Legendas claras**: Fácil interpretação

---

## Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:

1. Reportar bugs
2. Sugerir novas funcionalidades
3. Melhorar a documentação
4. Enviar pull requests

### Como Contribuir
```bash
# Fork o projeto
# Crie sua branch
git checkout -b feature/MinhaFuncionalidade

# Commit suas mudanças
git commit -m 'Adiciona nova funcionalidade'

# Push para a branch
git push origin feature/MinhaFuncionalidade

# Abra um Pull Request
```

---

## 📄 Licença

Este projeto está sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

## Autora

**Juliane Helanski**

- Email: [julianhelanski@gmail.com]
- LinkedIn: [linkedin.com/in/juliane-helanski-737314234]
- GitHub: [@julianehelanski]

---

## Agradecimentos

- **SciELO** - Scientific Electronic Library Online
- **CAPES** - Coordenação de Aperfeiçoamento de Pessoal de Nível Superior
- Comunidade Python científico
- Bibliotecas open-source utilizadas

---

## Citação

Se você usar este código em sua pesquisa, por favor cite:

```bibtex
@software{helanski2025analise_ia,
  author = {Helanski, Juliane},
  title = {Análise Bibliométrica: Inteligência Artificial na Produção Científica Brasileira},
  year = {2025},
  publisher = {GitHub},
  url = {https://github.com/seu-usuario/analise-ia-cientifica-brasil}
}
```

---

## Estatísticas do Projeto

![GitHub stars](https://img.shields.io/github/stars/seu-usuario/analise-ia-cientifica-brasil)
![GitHub forks](https://img.shields.io/github/forks/seu-usuario/analise-ia-cientifica-brasil)
![GitHub issues](https://img.shields.io/github/issues/seu-usuario/analise-ia-cientifica-brasil)

---

## Próximos Passos

- [ ] Interface gráfica (GUI)
- [ ] Análise de co-autoria
- [ ] Mapeamento de redes de citação
- [ ] Dashboard interativo (Plotly/Dash)
- [ ] Análise de sentimento em resumos
- [ ] Integração com outras bases (Scopus, Web of Science)
- [ ] API para consulta automatizada

---

## FAQ

**P: Posso usar com outras bases de dados?**  
R: Sim! Basta adaptar as funções de leitura para o formato da sua base.

**P: Os gráficos podem ser editados?**  
R: Sim, todos os parâmetros visuais são facilmente customizáveis no código.

**P: Funciona em Mac/Linux?**  
R: Sim, apenas ajuste os caminhos dos arquivos (use `/` em vez de `\`).

**P: Preciso de conhecimento em Python?**  
R: Básico. Os scripts são bem comentados e fáceis de executar.

---

<div align="center">

Made with ❤️ and 🐍 Python

</div>
