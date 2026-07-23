# Análise de Inadimplência de Carteira de Crédito

## 📌 Objetivo do Projeto

Este projeto consiste na análise de uma carteira de crédito de uma fintech de concessão de empréstimos online. O objetivo principal foi identificar a taxa de inadimplência geral, mapear quais segmentos de clientes apresentam um risco significativamente superior à média e, por fim, propor recomendações estratégicas fundamentadas na análise de *trade-offs* (relação de perda de receita vs. mitigação de risco).

---

## 💻 Tecnologias Utilizadas

* **SQL:** Extração, manipulação e agregação dos dados.
* **Microsoft Excel:** Criação de tabelas dinâmicas, tratamento e criação de faixas (*binning*).
* **Microsoft PowerPoint:** Elaboração do *storytelling* e apresentação dos resultados para stakeholders.
* **PowerBI:** Dashboard para visualização de dadps.
* **GitHub:** Versionamento de código e documentação.

---

## 📊 Base de Dados

O estudo foi realizado utilizando a base de dados `case_inadimplencia_dataset.csv`, que contém informações de **5.000 clientes** (onde cada linha representa 1 contrato de empréstimo).

* **Público-alvo:** Classes C e D.
* **Definição de Inadimplência:** Atraso igual ou superior a 90 dias (`inadimplente_90d = 1`).

### Dicionário de Dados

| Coluna | Tipo | Descrição |
| --- | --- | --- |
| `id_cliente` | Texto | Identificador único do cliente/contrato. |
| `data_contratacao` | Data | Data em que o crédito foi concedido. |
| `idade` | Inteiro | Idade do cliente no momento da contratação. |
| `sexo` | Categórico | Gênero do cliente (F / M). |
| `regiao` | Categórico | Região do Brasil (Sudeste, Nordeste, Sul, Norte, Centro-Oeste). |
| `renda_mensal` | Inteiro | Renda mensal declarada (R$). |
| `classe_social` | Categórico | Classe social estimada (C ou D). |
| `score_interno` | Inteiro | Score de crédito interno (0 a 1000). Quanto maior, melhor o perfil. |
| `canal_aquisicao` | Categórico | Canal de origem: App Próprio, Site, Indicação, Mídia Paga, Parceiro Marketplace A, Parceiro Marketplace B. |
| `num_emprestimos_anteriores` | Inteiro | Quantidade de empréstimos anteriores (0 = primeiro empréstimo). |
| `tempo_relacionamento_dias` | Inteiro | Dias de relacionamento do cliente com a empresa no momento da concessão. |
| `possui_restricao` | Binário | 1 = restrição ativa no momento da concessão; 0 = sem restrição. |
| `valor_solicitado` | Inteiro | Valor do empréstimo concedido (R$). |
| `prazo_meses` | Inteiro | Número de parcelas pactuadas (3, 6, 9 ou 12). |
| `taxa_juros_am` | Decimal | Taxa de juros ao mês (ex: 0,12 = 12% a.m.). |
| `valor_parcela` | Decimal | Valor da parcela mensal (R$). |
| `comprometimento_renda` | Decimal | Proporção da parcela sobre a renda mensal (ex: 0,30 = 30%). |
| `finalidade` | Categórico | Motivo do empréstimo (Pagar dívidas, Reforma, Saúde, Consumo, Emergência, Educação). |
| `dias_atraso_max` | Inteiro | Maior atraso registrado no contrato (em dias). |
| `inadimplente_90d` | Binário | **Variável-Alvo.** 1 = Inadimplente (atraso de 90+ dias); 0 = Adimplente. |

---

## 🎯 Perguntas de Negócio

Para direcionar as análises, buscou-se responder às seguintes questões:

1. Qual é a taxa de inadimplência consolidada de todo o portfólio?
2. Existem segmentos específicos (canais, perfis, scores) cuja inadimplência fique claramente acima da média do portfólio?
3. Quais ações estratégicas devem ser tomadas para mitigar as perdas e quais são os seus respectivos impactos financeiros (*trade-offs*)?

---

## ⚙️ Tratamento e Agrupamento de Dados (*Binning*)

Para facilitar a análise de distribuição e identificação de padrões de comportamento, as variáveis numéricas contínuas foram agrupadas em faixas (intervalos):

| Variável | Faixas / Intervalos |
| --- | --- |
| **Mês/Ano de Contratação** | `2023-07` a `2024-12` |
| **Faixa de Idade** | `0-20` | `21-30` | `31-40` | `41-50` | `51-60` | `60+` |
| **Faixa de Renda** | `R$ 0,00 - 1.000` a `R$ 5.000+` |
| **Faixa de Score** | `0-150` a `750+` |
| **Tempo de Relacionamento** | `0-120` a `520+` dias |
| **Valor Solicitado** | `R$ 0 - 400` a `> R$ 3.200` |
| **Taxa de Juros** | `0 - 9%` | `9 - 12%` | `12 - 15%` | `> 15%` a.m. |
| **Valor da Parcela** | `Até R$ 200` a `> R$ 750` |
| **Comprometimento de Renda** | `0 - 10%` a `> 40%` |
| **Dias de Atraso** | `0 - 45` a `> 225` dias |

---

## 💡 Principais Insights Mapeados

* **Inadimplência Elevada:** A taxa geral de inadimplência da carteira é de **18,10%**, patamar significativamente maior que a média recomendada de mercado (historicamente entre 8% e 15%).
* **Capital em Risco:** **18,55%** do volume total financeiro desembolsado na carteira foi direcionado a clientes que se tornaram inadimplentes.
* **Novos Clientes:** Clientes sem histórico de empréstimos anteriores e com menos de 120 dias de relacionamento concentram **40,22%** de todo o capital em risco.
* **Baixa Qualidade de Score:** **49,94%** dos clientes da base possuem score interno abaixo de 450 pontos, respondendo por **51,11%** do valor inadimplido.
* **Gargalo de Canal (Marketplace B):** O *Marketplace B* representa um volume relevante de originação de crédito (**11,29%** do valor emprestado), porém possui a pior inadimplência da base, atingindo alarmantes **32,69%**, mesmo representando apenas 11,38% da base de clientes.
* **Sazonalidade:** **67,75%** das ocorrências de inadimplência concentram-se em contratos gerados entre agosto, setembro e novembro de 2023.
* **Comprometimento de Renda:** Clientes que comprometem entre 30% e 40% da renda mensal na parcela possuem propensão de inadimplência de **24,40%**.
* **Risco de Negativação Prévia:** A inadimplência entre clientes que já possuíam restrições ativas no momento da contratação é de **27,63%**.

---

## 📋 Recomendações e Análise de Trade-off

Abaixo estão detalhadas as propostas de políticas de crédito avaliadas para reduzir as perdas financeiras e seus respectivos impactos comerciais:

### 1. Bloqueio de Clientes com Restrição Ativa (se Score Interno < 300 OR Relacionamento < 120 dias)

* 👍 **Prós (Ganho):** Evita que **4,45%** dos recursos da carteira sejam direcionados a perdas.
* 👎 **Contras (Custo):** Reduz em **11,92%** a base total de clientes ativos.

### 2. Suspensão de Empréstimos para Score Interno < 300

* 👍 **Prós (Ganho):** Poupa **4,72%** do capital total que seria perdido.
* 👎 **Contras (Custo):** Impacta negativamente a base com uma redução de **4,84%** de clientes.

### 3. Limitação de Limite de Crédito para Novos Clientes (sem empréstimos anteriores e < 120 dias de casa)

* 👍 **Prós (Ganho):** Reduz a exposição ao risco salvando **7,46%** do capital geral sob risco.
* 👎 **Contras (Custo):** Impacta a experiência inicial de **20,50%** da carteira de clientes.

### 4. Revisão e Negociação Contratual com o Marketplace B

* 👍 **Prós (Ganho):** Economia direta de **3,70%** dos recursos totais desperdiçados na inadimplência.
* 👎 **Contras (Custo):** Afeta **11,38%** do volume transacionado total da fintech.

---

## 🚀 Próximos Passos

1. **Utilização de python:** Construção de um código para realização de análise exploratória dos dados.
2. **Modelagem Preditiva:** Construção de um modelo de *Machine Learning* para classificação de risco de crédito (utilizando algoritmos como *Regressão Logística* ou *XGBoost*).
