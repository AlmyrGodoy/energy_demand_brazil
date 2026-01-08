# Metodologia

Este projeto analisa a demanda por energia elétrica no setor industrial brasileiro por meio de métodos econométricos aplicados a séries temporais mensais.

A abordagem metodológica combina teoria econômica, análise quantitativa e modelagem econométrica, permitindo a estimação de elasticidades da demanda e a validação estatística dos resultados.

---

## Delineamento da Pesquisa

- **Natureza**: Pesquisa básica  
- **Abordagem**: Quantitativa  
- **Objetivo**: Descritivo  
- **Método**: Análise econométrica de séries temporais  

O período analisado compreende **1997 a 2023**, com atenção ao contexto histórico e a possíveis quebras estruturais que afetam a demanda por energia elétrica no setor industrial.

---

## Fonte e Descrição dos Dados

Os dados utilizados são **mensais** e foram obtidos a partir da base **IPEADATA**.

### Variáveis Utilizadas

- **Consumo de energia elétrica industrial** (MWh)  
- **Tarifa média de energia elétrica** (R$/MWh)  
- **Produto Interno Bruto (PIB)** – proxy de renda  
- **Índice de importações de derivados do petróleo** – proxy de bem substituto  
- **Índice de preços (IGP-DI / IPCA)** – utilizado para deflação  

As variáveis monetárias foram deflacionadas para obtenção de valores reais.

---

## Fundamentação Teórica

A modelagem da demanda baseia-se na **Teoria Neoclássica da Demanda** (Varian, 2015), segundo a qual a quantidade demandada depende da renda, do preço do próprio bem e do preço de bens substitutos:

D = f(Y, P, PBS)


Sinais esperados dos coeficientes:

- Elasticidade-renda (Y): positiva  
- Elasticidade-preço (P): negativa  
- Elasticidade-preço cruzada (PBS): positiva  

---

## Especificação do Modelo Econométrico

Utiliza-se um modelo do tipo **log-log**, conforme Gujarati e Porter (2011), que permite interpretar diretamente os coeficientes como elasticidades:

ln(D_t) = β₀ − β₁ ln(P_t) + β₂ ln(Y_t) + β₃ ln(PBS_t) + u_t


Onde:

- `D_t`: demanda por energia elétrica industrial  
- `P_t`: tarifa média de energia elétrica  
- `Y_t`: PIB  
- `PBS_t`: preço dos derivados do petróleo (Preço do Bem substituto) 
- `u_t`: termo de erro  

---

## Testes Econométricos

Para validação do modelo, foram realizados os seguintes testes:

### Normalidade dos Resíduos
- Histograma  
- Teste de Jarque-Bera  

### Multicolinearidade
- Fator de Inflação da Variância (VIF)  

### Heterocedasticidade
- Teste de White  
- Teste de Breusch-Pagan  

### Autocorrelação
- Teste de Durbin-Watson  
- Teste das Carreiras (Geary)  

### Estacionariedade
- Análise gráfica  
- Correlograma  
- Testes de raiz unitária (ADF e KPSS)  

---

## Ferramentas Utilizadas

- **Python** (pandas, numpy, statsmodels) – tratamento e preparação dos dados  
- **Gretl** – estimação econométrica e testes estatísticos  
- **Git e GitHub** – versionamento, organização e reprodutibilidade  

---

## Reprodutibilidade

Todas as etapas de tratamento dos dados, construção das variáveis e estimação dos modelos estão documentadas no repositório.  
A estrutura do projeto segue boas práticas de ciência de dados, separando dados brutos, dados processados e códigos-fonte.

---
