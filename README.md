# 📊 Demanda de Energia Elétrica no Setor Industrial Brasileiro

## 📌 Descrição do Projeto

Este projeto é uma ampliação do meu TCC do curso de Ciências Econômicas - UFSM - Palmeira das Missões, que foi orientado pelo Doutor Cézar Augusto Pereira dos Santos e avaliado pela banca composta pelos professores Doutores Nilson Luiz Costa e Tanice Andreatta, no qual, foi apresentado no dia 16/12/2024 e que tive a felicidade de obter nota máxima. 

O projeto é uma evolução metodológica do meu TCC (O arquivo antigo está na pasta docs), reorganizado segundo boas práticas de Engenharia de Dados e Ciência de Dados, com versionamento em GitHub e estrutura modular de código.

## 🎯 Objetivo Geral

Este projeto tem como objetivo analisar, modelar e prever a demanda de energia elétrica no setor industrial brasileiro, utilizando técnicas de econometria aplicada, engenharia e ciência de dados. O trabalho foi desenvolvido a partir de dados oficiais do IPEADATA, com foco na construção de um pipeline reprodutível de coleta, tratamento, transformação e análise de séries temporais econômicas.

---

## 🎯 Objetivos Específicos

## Engenharia de Dados:

- ETL
- Estruturar código reproduzível
- Pipeline de dados
    
## Ciência de Dados e Econometria:

### Regressão Linear Múltipla (OLS/MQO)
- Estimar a relação da demanda de energia elétrica industrial no Brasil com MQO, através das variáveis Independentes:
- Nível de atividade econômica (PIB)
- Tarifa média de energia elétrica industrial 
- Índice de Preço de Importações dos derivados de petróleo (Produto Substituto)
- Choques estruturais e eventos extraordinários (Apagão elétrico de 2001, erro estatístico de 2006, Crise financeira e econômica de 2008 e Pandemia de 2020)

### ARIMA/ARIMAX/SARIMA
- Prever a demanda de Energia Elétrica Industrial através da metodologia ARIMA/Box Jenkins e Derivados
- 
---

## 📚 Fundamentação Metodológica

O projeto utiliza fundamentos de:
- Econometria de Séries Temporais - Regressão Linear Múltipla 
- Modelos log-log (elasticidades)
- Deflação de séries monetárias
- Testes de estacionariedade, Autocorrelação, Normalidade, Heterocedasticidade e Multicolinearidade
- Modelagem econométrica e análise de choques econômicos

Eventos estruturais relevantes são capturados por variáveis dummy, tais como:
- Apagão de 2001
- Erro estatístico de 2006
- Crise financeira internacional de 2008/2009
- Pandemia de COVID-19 em 2020

---

## 🗂️ Estrutura de Diretórios do Projeto

```
energy-demand/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── data/
│   ├── raw/
│   ├── interim/
│   └── processed/
│
├── notebooks/
│   ├── 01_exploratory_analysis.ipynb
│   ├── 02_stationarity_tests.ipynb
│   ├── 03_model_specification.ipynb
│   ├── 04_model_estimation.ipynb
│   └── 05_forecasting.ipynb
│
├── src/
│   ├── __init__.py
│   ├── data_ingestion.py
│   ├── data_cleaning.py
│   ├── features.py
│   ├── stationarity.py
│   ├── models.py
│   ├── diagnostics.py
│   └── visualization.py
│
├── results/
│   ├── tables/
│   └── figures/
│
├── docs/
│   ├── methodology.md
│   └── references.md
│
└── scripts/
    └── run_pipeline.py
```

## 📥 Fontes de Dados

Os dados utilizados são provenientes do **IPEA Data**, acessados via API:

- Consumo de energia elétrica industrial
- Tarifa média de energia elétrica industrial
- Produto Interno Bruto (PIB)
- Importações de derivados de petróleo
- Índice Geral de Preços – Disponibilidade Interna (IGP-DI)

Todos os dados possuem frequência mensal.

---

## 🔄 Pipeline de Dados

O fluxo do projeto segue as seguintes etapas:

1. **Coleta de dados (`data_ingestion.py`)**
   - Extração automática via API do IPEA
   - Armazenamento dos dados brutos em `data/raw`

2. **Tratamento e consolidação (`data_cleaning.py`)**
   - Padronização de datas
   - Conversão de unidades (GWh → MWh)
   - Consolidação das séries em base única

3. **Transformações econômicas (`features.py`)**
   - Deflação de variáveis monetárias pelo IGP-DI
   - Criação de variáveis dummy para choques estruturais

4. **Análises econométricas (`notebooks`)**
   - Testes de estacionariedade
   - Especificação e estimação de modelos
   - Diagnósticos estatísticos

---

## ⚙️ Tecnologias Utilizadas

O projeto foi desenvolvido utilizando as seguintes tecnologias e bibliotecas:

- **Python 3** – linguagem principal para análise de dados e modelagem econométrica  
- **pandas** – manipulação, limpeza e organização de séries temporais  
- **numpy** – operações matemáticas e transformações numéricas  
- **statsmodels** – estimação de modelos econométricos (MQO, testes estatísticos, diagnósticos)  
- **scipy** – suporte a métodos estatísticos e testes complementares  
- **patsy** – construção de matrizes de regressão e especificação de modelos  
- **matplotlib** – visualização de séries temporais e resultados econométricos  
=- **ipeadatapy** – extração automatizada de dados macroeconômicos via API do IPEA  
- **Git e GitHub** – controle de versão, organização e reprodutibilidade do projeto


## ▶️ Como Executar o Projeto

1. Instale as dependências:
```bash
pip install -r requirements.txt


