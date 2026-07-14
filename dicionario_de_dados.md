# Dicionário de Dados — Case Inadimplência

Base: `case_inadimplencia_dataset.csv` · 5.000 clientes · 1 linha = 1 contrato de empréstimo.

Contexto: fintech de crédito online para o público C/D. Cada linha representa um empréstimo concedido; a coluna-alvo indica se o cliente ficou inadimplente (atraso de 90+ dias).

| Coluna | Tipo | Descrição |
|---|---|---|
| `id_cliente` | texto | Identificador único do cliente/contrato. |
| `data_contratacao` | data | Data em que o crédito foi concedido. |
| `idade` | inteiro | Idade do cliente no momento da contratação (anos). |
| `sexo` | categórico | F / M. |
| `regiao` | categórico | Região do Brasil (Sudeste, Nordeste, Sul, Norte, Centro-Oeste). |
| `renda_mensal` | inteiro (R$) | Renda mensal declarada. |
| `classe_social` | categórico | Classe estimada (C ou D). |
| `score_interno` | inteiro (0–1000) | Score de crédito interno na concessão. Quanto maior, melhor o perfil. |
| `canal_aquisicao` | categórico | Como o cliente chegou: App Próprio, Site, Indicação, Mídia Paga, Parceiro Marketplace A, Parceiro Marketplace B. |
| `num_emprestimos_anteriores` | inteiro | Quantos empréstimos o cliente já teve antes deste (0 = primeiro empréstimo). |
| `tempo_relacionamento_dias` | inteiro | Dias de relacionamento do cliente com a empresa na concessão. |
| `possui_restricao` | binário | 1 = tinha restrição/negativação de crédito no momento da concessão; 0 = não. |
| `valor_solicitado` | inteiro (R$) | Valor do empréstimo concedido. |
| `prazo_meses` | inteiro | Número de parcelas (3, 6, 9 ou 12). |
| `taxa_juros_am` | decimal | Taxa de juros ao mês (ex.: 0,12 = 12% a.m.). |
| `valor_parcela` | decimal (R$) | Valor da parcela mensal. |
| `comprometimento_renda` | decimal | Parcela ÷ renda mensal (ex.: 0,30 = 30% da renda comprometida). |
| `finalidade` | categórico | Motivo declarado: Pagar dívidas, Reforma, Saúde, Consumo, Emergência, Educação. |
| `dias_atraso_max` | inteiro | Maior atraso registrado no contrato (dias). |
| `inadimplente_90d` | binário | **VARIÁVEL-ALVO.** 1 = inadimplente (atraso de 90+ dias); 0 = adimplente. |

> Observação: os dados são **fictícios**, gerados apenas para fins de avaliação. Qualquer semelhança com clientes reais é coincidência.
