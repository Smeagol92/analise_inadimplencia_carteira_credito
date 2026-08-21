#%%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math    

## IMPORTAÇÃO DE BANCO DE DADOS

df = pd.read_csv("C:/Users/Francisco/Desktop/case_enova/case_inadimplencia_dataset.csv")

## TRATAMENTO E CATEGORIZAÇÃO DE DADOS

df['data_contratacao'] = pd.to_datetime(df['data_contratacao']).dt.to_period('M')
df['taxa_juros_am'] = 100.00*df['taxa_juros_am']
df['comprometimento_renda'] = 100.00*df['comprometimento_renda']
df['faixa_idade'] = pd.cut(df['idade'],bins=[0,20,30,40,50,60,70])
df['faixa_renda_mensal'] = pd.cut(df['renda_mensal'],bins=[0,1000,2000,3000,4000,5000,6000])
df['faixa_score_interno'] = pd.cut(df['score_interno'],bins=[0,150,300,450,600,750,1000])
df['faixa_tempo_relacionamento_dias'] = pd.cut(df['tempo_relacionamento_dias'],bins=[0,120,240,360,480,600,720,840,960])
df['faixa_valor_solicitado'] = pd.cut(df['valor_solicitado'],bins=[0,400,800,1200,1600,2000,2400,2800,3200])
df['faixa_taxa_juros_am'] = pd.cut(df['taxa_juros_am'],bins=[3,6,9,12,15,18])
df['faixa_valor_parcela'] = pd.cut(df['valor_parcela'],bins=[0,200,400,600,800,1000,1200,1400])
df['faixa_comprometimento_renda'] = pd.cut(df['comprometimento_renda'],bins=[0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150])
df['faixa_dias_atraso_max'] = pd.cut(df['dias_atraso_max'], bins=(0, 45, 90, 135, 180, 225, 270), include_lowest=True)
df['status'] = df['inadimplente_90d'].map({1: 'inadimplente', 0: 'adimplente'})

## GERAÇÃO DE DATAFRAME TOTAL COM COLUNAS SELECIONADAS

df_total = df[[
    "id_cliente",        
    "data_contratacao",
    "idade",
    'faixa_idade',
    'sexo',
    'regiao',
    "renda_mensal",
    'faixa_renda_mensal',
    'classe_social',
    "score_interno",
    'faixa_score_interno',
    'canal_aquisicao',
    "num_emprestimos_anteriores",
    "tempo_relacionamento_dias",
    "faixa_tempo_relacionamento_dias",
    "valor_solicitado",
    'faixa_valor_solicitado',
    'possui_restricao',
    "prazo_meses",
    "taxa_juros_am",
    'faixa_taxa_juros_am',
    "valor_parcela",
    'faixa_valor_parcela',
    "comprometimento_renda",
    "faixa_comprometimento_renda",
    'finalidade',
    'dias_atraso_max',
    'faixa_dias_atraso_max',
    'status',
    'inadimplente_90d',
    ]]

## GERAÇÃO DE DATAFRAMES PARA ADIMPLENTES E INADIMPLENTES

filtro_1 = (df_total["inadimplente_90d"] == 1)
df_inadimplencia = df_total[filtro_1]

filtro_0 = (df_total["inadimplente_90d"] == 0)
df_adimplencia = df_total[filtro_0]

#%%

## CALCULO DA INADIMPLÊNCIA GERAL = 0.181

tx_inadimplencia_geral = df_total['inadimplente_90d'].mean()
count_clientes_inadim = df_total['inadimplente_90d'].sum()
count_clientes_geral = df_total['inadimplente_90d'].count()
sum_recursos_total = df_total['valor_solicitado'].sum()
sum_recursos_inadim = df_total.loc[df_total['inadimplente_90d'] == 1, 'valor_solicitado'].sum()


print('Taxa de inadimplencia:',(100*tx_inadimplencia_geral).round(3)), 
print('Total de clientes:',count_clientes_geral),
print('Total de clientes inadimplentes:',count_clientes_inadim),
print('Total de recursos destinados:',sum_recursos_total),
print('Total de recursos destinados com inadimplentes:',sum_recursos_inadim)
#%%


## CALCULO DA INADIMPLÊNCIA POR CATEGORIAS E PORCENTAGEM DE CLIENTES POR CATEGORIA

list = ['data_contratacao', 
        'faixa_idade', 
        'sexo', 
        'regiao', 
        'faixa_renda_mensal', 
        'canal_aquisicao', 
        'num_emprestimos_anteriores', 
        'faixa_tempo_relacionamento_dias', 
        'faixa_valor_solicitado', 
        'possui_restricao', 
        'prazo_meses', 
        'faixa_taxa_juros_am', 
        'faixa_comprometimento_renda', 
        'finalidade', 
        'classe_social', 
        'faixa_score_interno', 
        'faixa_valor_parcela'
]

for i in list:
        globals()[f'tx_inadimplencia_{i}'] = pd.DataFrame({'class': i, 
                                         'tx_inadimplencia': df_total.groupby(i)['inadimplente_90d'].mean(), 
                                         'pctg_clientes': df_total.groupby(i)['inadimplente_90d'].count()/df_total['inadimplente_90d'].count()}).sort_values(by='tx_inadimplencia', ascending=False)

df_tx_inadimplencia = pd.concat([
        globals()[f'tx_inadimplencia_{i}'] for i in list
], ignore_index=False).sort_values(by='tx_inadimplencia', ascending=False)

df_pctg_inadimp = df_tx_inadimplencia[df_tx_inadimplencia['tx_inadimplencia'] >= tx_inadimplencia_geral].round(4).sort_values(by='tx_inadimplencia', ascending=False)
df_pctg_inadimp
#%%
## GERAÇÃO DE DATAFRAME COM PROBABILIDADE DE INADIMPLÊNCIA POR CATEGORIA

df_prob = pd.DataFrame({
    'class': df_pctg_inadimp['class'],
    'tx_inadimplencia': 100*df_pctg_inadimp['tx_inadimplencia'],
    'pctg_clientes': 100*df_pctg_inadimp['pctg_clientes'],
    'prob_inadimp': 100*(df_pctg_inadimp['tx_inadimplencia'] * df_pctg_inadimp['pctg_clientes'])
}).sort_values(by='tx_inadimplencia', ascending=False)

filtro_prob = df_prob['prob_inadimp'] >= 1
df_prob = df_prob[filtro_prob].round(2)
df_prob
#%%

## ORDENANDO DATAFRAME DE PROBABILIDADE DE INADIMPLÊNCIA POR CATEGORIA

df_prob = df_prob.sort_values(by='class', ascending=False)

## PRIORIZAÇÃO DE INADIMPLÊNCIA ACIMA DE 22%

filtro_prob = df_prob['tx_inadimplencia'] >= 22
df_prob = df_prob[filtro_prob].round(2)
df_prob

#%%
    
## AMPLIANDO BANDA DE CATEGORIAS PARA VISUALIZAÇÃO DE INADIMPLÊNCIA
from datetime import datetime as dt

## RETORNANDO O MÊS DE CONTRATAÇÃO PARA ANÁLISE DE INADIMPLÊNCIA POR MÊS
df['faixa_valor_solicitado'] = pd.cut(df['valor_solicitado'],bins=[0,400,800,1200,1600,2000,2400,2800,3200])
df['faixa_valor_parcela'] = pd.cut(df['valor_parcela'],bins=[0,200,600,1000,1200,1400])
df['faixa_taxa_juros_am'] = pd.cut(df['taxa_juros_am'],bins=[3,6,9,12,18])
df['faixa_score_interno'] = pd.cut(df['score_interno'],bins=[0,450,600,750,1000])
df['faixa_renda_mensal'] = pd.cut(df['renda_mensal'],bins=[0,2000,3000,4000,5000,6000])
df['faixa_idade'] = pd.cut(df['idade'],bins=[0,30,40,50,60,70])
df['faixa_comprometimento_renda'] = pd.cut(df['comprometimento_renda'],bins=[0,10,20,30,50,60,70,80,90,100,110,120,130,140,150])

df_total = df[[
    "id_cliente",        
    "data_contratacao",
    "idade",
    'faixa_idade',
    'sexo',
    'regiao',
    "renda_mensal",
    'faixa_renda_mensal',
    'classe_social',
    "score_interno",
    'faixa_score_interno',
    'canal_aquisicao',
    "num_emprestimos_anteriores",
    "tempo_relacionamento_dias",
    "faixa_tempo_relacionamento_dias",
    "valor_solicitado",
    'faixa_valor_solicitado',
    'possui_restricao',
    "prazo_meses",
    "taxa_juros_am",
    'faixa_taxa_juros_am',
    "valor_parcela",
    'faixa_valor_parcela',
    "comprometimento_renda",
    "faixa_comprometimento_renda",
    'finalidade',
    'dias_atraso_max',
    'faixa_dias_atraso_max',
    'status',
    'inadimplente_90d',
    ]]


filtro_1 = (df_total["inadimplente_90d"] == 1)
df_inadimplencia = df_total[filtro_1]

filtro_0 = (df_total["inadimplente_90d"] == 0)
df_adimplencia = df_total[filtro_0]

for i in list:
        globals()[f'tx_inadimplencia_{i}'] = pd.DataFrame({'class': i, 
                                         'tx_inadimplencia': df_total.groupby(i)['inadimplente_90d'].mean(), 
                                         'pctg_clientes': df_total.groupby(i)['inadimplente_90d'].count()/df_total['inadimplente_90d'].count()}).sort_values(by='tx_inadimplencia', ascending=False)

df_tx_inadimplencia = pd.concat([
        globals()[f'tx_inadimplencia_{i}'] for i in list
], ignore_index=False).sort_values(by='tx_inadimplencia', ascending=False)

df_pctg_inadimp = df_tx_inadimplencia[df_tx_inadimplencia['tx_inadimplencia'] >= tx_inadimplencia_geral].round(6).sort_values(by='tx_inadimplencia', ascending=False)

df_prob = pd.DataFrame({
    'class': df_pctg_inadimp['class'],
    'tx_inadimplencia': 100*df_pctg_inadimp['tx_inadimplencia'],
    'pctg_clientes': 100*df_pctg_inadimp['pctg_clientes'],
    'prob_inadimp': 100*(df_pctg_inadimp['tx_inadimplencia'] * df_pctg_inadimp['pctg_clientes'])
}).sort_values(by='prob_inadimp', ascending=False)

filtro_prob = df_prob['prob_inadimp'] >= 1
df_prob = df_prob[filtro_prob].round(2)

df_prob.sort_values(by='prob_inadimp', ascending=False)

#%%

## DEFINIÇÃO DE FAIXAS DE ALERTAS DE INADIMPLÊNCIA

# Até 18%: Faixa atual da carteira, exigindo monitoramento padrão e régua de cobrança preventiva.
# De 18,1% a 22%: Alerta amarelo. O perfil do cliente começa a apresentar desvios do comportamento saudável.
# Acima de 22% a 25%: Alerta vermelho. Risco elevado de perda, necessitando revisão de limites de crédito.
# Acima de 25%: Risco crítico. Ação imediata com restrição de novas vendas a prazo e renegociação forçada.

#%%

## PRIORIDADE 0 - ACIMA DE 25% - RISCO CRÍTICO

df_prob[df_prob['tx_inadimplencia'] >= 25]

## FAIXA DE SCORE INTERNO - DE 150 A 450
## CLIENTES QUE POSSUAM RESTRIÇÃO
## CLIENTES QUE NÃO TENHAM ADQUIRIDO EMPRÉSTIMOS ANTERIORES
## EMPRÉSTIMOS ADQUIRIDOS PELO MARKETPLACE B

#%%

## ANÁLISE DA CARTEIRA QUE PELO SCORE INTERNO

df_total.groupby('faixa_score_interno').agg({
    'renda_mensal':['mean','std','max','min','median'],
    'tempo_relacionamento_dias':['mean','std','max','min','median'],
    'inadimplente_90d':['mean']
}).round(3).T

# O TEMPO DE RELACIONAMENTO É MUITO MENOR POR QUEM TEM DE 0 A 450
#%%

cross_score_relacionamento_total = pd.crosstab(
    df_total['faixa_score_interno'],
    df_total['faixa_tempo_relacionamento_dias']
)


cross_score_relacionamento_inadimplencia = pd.crosstab(
    df_inadimplencia['faixa_score_interno'],
    df_inadimplencia['faixa_tempo_relacionamento_dias']
)


cross_inadimp_total = (cross_score_relacionamento_inadimplencia)**3/cross_score_relacionamento_total
sns.heatmap(cross_inadimp_total, annot=True, cmap='coolwarm')

plt.show()

#%%

loss_client = cross_score_relacionamento_total.iloc[0, 0]+cross_score_relacionamento_total.iloc[0, 1]
loss_inadimp = cross_score_relacionamento_inadimplencia.iloc[0, 0]+cross_score_relacionamento_inadimplencia.iloc[0, 1]
loss_cliente_total = loss_client/count_clientes_geral

nova_inadimp = (count_clientes_inadim-loss_inadimp)/(count_clientes_geral-loss_client)

loss_recursos_inadimp = df_total[(df_total['score_interno'] <= 450) & (df_total['tempo_relacionamento_dias'] <= 240) & (df_total['inadimplente_90d'] == 1)]['valor_solicitado'].sum()
loss_recursos_total = df_total[(df_total['score_interno'] <= 450) & (df_total['tempo_relacionamento_dias'] <= 240)]['valor_solicitado'].sum()


print("Nova inadimplência:",(100*nova_inadimp).round(2),"%"),
print("Recuo da inadimplencia:",(100*(1-(nova_inadimp/tx_inadimplencia_geral))).round(2),"%"),
print("Recuo da carteira de clientes:",(100*loss_cliente_total).round(2),"%"),
print("Recuo da disponiblização de recursos:",(100*(loss_recursos_total/sum_recursos_total)).round(2),"%"),

#%%

# DENTRO DO GRUPO SCORE INTERNO DE 0 A 450 
# NEGAR EMPRESTIMO A QUEM TEM TEMPO DE RELACIONAMENTO DE 0 A 240 DIAS
# REDUZ A INADIMPLÊNCIA DE 18,10% PARA 15,12%
# MAS REPRESENTA UMA PERDA DE 14,96% NA CARTEIRA DE CLIENTES
# E RETRAÇÃO DE 15,08% NOS RECURSOS SOLICITADOS

## =======================================================================
#%%

## CLIENTES QUE POSSUAM RESTRIÇÃO

df_inadimplencia.groupby(['possui_restricao']).agg({
    'valor_solicitado':['mean','median'],
    'inadimplente_90d':['mean']
}).round(2).T

## VALOR SOLICITADO POR QUEM TEM RESTRIÇÃO E INADIMPLENCIA É MAIOR
## DO QUE QUEM TEM RESTRIÇÃO E É ADIMPLENTE

#%%

cross_restricao_valor_solicitado = pd.crosstab(
    df_total['possui_restricao'],
    df_total['faixa_valor_solicitado'],
    normalize='columns'
)

cross_restricao_valor_solicitado=cross_restricao_valor_solicitado.T

cross_restricao_valor_solicitado_inadimplencia = pd.crosstab(
    df_inadimplencia['possui_restricao'],
    df_inadimplencia['faixa_valor_solicitado'],
    normalize='columns'
)

cross_restricao_valor_solicitado_inadimplencia=cross_restricao_valor_solicitado_inadimplencia.T

cross_inadimp_total = (cross_restricao_valor_solicitado_inadimplencia)**3/cross_restricao_valor_solicitado

sns.heatmap(cross_inadimp_total, annot=True, cmap='coolwarm')

plt.show()

#%%
cross_restricao_valor_solicitado = pd.crosstab(
    df_total['possui_restricao'],
    df_total['faixa_valor_solicitado']
)

cross_restricao_valor_solicitado=cross_restricao_valor_solicitado.T

cross_restricao_valor_solicitado_inadimplencia = pd.crosstab(
    df_inadimplencia['possui_restricao'],
    df_inadimplencia['faixa_valor_solicitado']
)

cross_restricao_valor_solicitado_inadimplencia=cross_restricao_valor_solicitado_inadimplencia.T

loss_client = cross_restricao_valor_solicitado.iloc[7, 1]
loss_inadimp = cross_restricao_valor_solicitado_inadimplencia.iloc[7, 1] 
loss_cliente_total = loss_client/count_clientes_geral
nova_inadimp = (count_clientes_inadim-loss_inadimp)/(count_clientes_geral-loss_client)

loss_recursos_inadimp = df_total[(df_total['valor_solicitado'] > 2800) & (df_total['valor_solicitado'] <= 3200) & (df_total['possui_restricao'] == 1) & (df_total['inadimplente_90d'] == 1)]['valor_solicitado'].sum()
loss_recursos_total = df_total[(df_total['valor_solicitado'] > 2800) & (df_total['valor_solicitado'] <= 3200) & (df_total['possui_restricao'] == 1)]['valor_solicitado'].sum()

print("Nova inadimplência:",(100*nova_inadimp).round(2),"%"),
print("Recuo da inadimplencia:",(100*(1-(nova_inadimp/tx_inadimplencia_geral))).round(2),"%"),
print("Recuo da carteira de clientes:",(100*loss_cliente_total).round(2),"%"),
print("Recuo da disponiblização de recursos:",(100*(loss_recursos_total/sum_recursos_total)).round(2),"%"),

## DENTRO DO GRUPO DE CLIENTES QUE POSSUEM RESTRIÇÃO
## NEGAR EMPRESTIMO A QUEM SOLICITOU ENTRE R$ 2.800,00 E R$ 3.200,00
## REDUZ A INADIMPLÊNCIA DE 18,10% PARA EM 17,78%
## MAS REPRESENTA UMA PERDA DE 1,92% NA CARTEIRA DE CLIENTES
## E RETRAÇÃO DE 3,50% NOS RECURSOS SOLICITADOS (R$ 279.000,00)

#%%

## ANALISE DE INADIMPLENCIA PELO NUMERO DE EMPRESTIMOS ANTERIORES

df_inadimplencia.groupby('num_emprestimos_anteriores').agg({
    'id_cliente':['count'],
    'score_interno':['mean','std','max','min','median'],
    'tempo_relacionamento_dias':['mean','std','max','min','median']
}).round(3).T

#%%

cross_emp_anteriores_score = pd.crosstab(
    df_total['num_emprestimos_anteriores'],
    df_total['faixa_score_interno'],
    normalize='all'
)

cross_emp_anteriores_score_inadimplencia = pd.crosstab(
    df_inadimplencia['num_emprestimos_anteriores'],
    df_inadimplencia['faixa_score_interno'],
    normalize='all'
)

cross_inadimp_total = (cross_emp_anteriores_score_inadimplencia)**3/cross_emp_anteriores_score

sns.heatmap(cross_inadimp_total, annot=True, cmap='coolwarm')

plt.show()

#%%
cross_emp_anteriores_score = pd.crosstab(
    df_total['num_emprestimos_anteriores'],
    df_total['faixa_score_interno']
)

cross_emp_anteriores_score=cross_emp_anteriores_score.T

cross_emp_anteriores_score_inadimplencia = pd.crosstab(
    df_inadimplencia['num_emprestimos_anteriores'],
    df_inadimplencia['faixa_score_interno']
)

cross_emp_anteriores_score_inadimplencia=cross_emp_anteriores_score_inadimplencia.T

loss_client = cross_emp_anteriores_score.iloc[0,0]
loss_inadimp = cross_emp_anteriores_score_inadimplencia.iloc[0,0]
loss_cliente_total = loss_client/count_clientes_geral
nova_inadimp = (count_clientes_inadim-loss_inadimp)/(count_clientes_geral-loss_client)
loss_recursos_inadimp = df_total[(df_total['score_interno'] <=450) & (df_total['num_emprestimos_anteriores'] == 0) & (df_total['inadimplente_90d']==1)]['valor_solicitado'].sum()
loss_recursos_total = df_total[(df_total['score_interno'] <=450) & (df_total['num_emprestimos_anteriores'] == 0) ]['valor_solicitado'].sum().sum()

print("Nova inadimplência:",(100*nova_inadimp).round(2),"%"),
print("Recuo da inadimplencia:",(100*(1-(nova_inadimp/tx_inadimplencia_geral))).round(2),"%"),
print("Recuo da carteira de clientes:",(100*loss_cliente_total).round(2),"%"),
print("Recuo da disponiblização de recursos:",(100*(loss_recursos_total/sum_recursos_total)).round(2),"%"),


## DENTRO DO GRUPO DE CLIENTES QUE NUNCA SOLICITARAM EMPRESTIMOS ANTERIORES E POSSUEM SCORE INTERNO DE 0 A 450
## NEGAR EMPRESTIMO A QUEM POSSUI DE 750 A 1000 PONTOS DE SCORE INTERNO
## AUMENTA A INADIMPLÊNCIA DE 18,10% PARA 18,14%
## MAS REPRESENTA UMA PERDA DE 0,78% NA CARTEIRA DE CLIENTES
## E RETRAÇÃO DE 0,8% NOS RECURSOS SOLICITADOS
#%%

#%% VERIFICAÇÃO DA HIPOTESE DE CLIENTES QUE NUNCA CONTRAIRAM EMPRESTIMOS
## E POSSUI POUCO TEMPO DE RELACIONAMENTO COM A EMPRESA

cross_emp_anteriores_tempo_relacionamento_inadimplencia = pd.crosstab(
    df_inadimplencia['num_emprestimos_anteriores'],
    df_inadimplencia['faixa_tempo_relacionamento_dias']
)

cross_emp_anteriores_tempo_relacionamento_inadimplencia=cross_emp_anteriores_tempo_relacionamento_inadimplencia.T

cross_emp_anteriores_tempo_relacionamento = pd.crosstab(
    df_total['num_emprestimos_anteriores'],
    df_total['faixa_tempo_relacionamento_dias']
)

cross_emp_anteriores_tempo_relacionamento=cross_emp_anteriores_tempo_relacionamento.T

cross_inadimp_total = (cross_emp_anteriores_tempo_relacionamento_inadimplencia)**3/cross_emp_anteriores_tempo_relacionamento

sns.heatmap(cross_inadimp_total, annot=True, cmap='coolwarm')

plt.show()

#%%

loss_client = df_total[(df_total['score_interno'] <= 450) & (df_total['tempo_relacionamento_dias'] <= 120) & (df_total['num_emprestimos_anteriores'] == 0)]['valor_solicitado'].count()
loss_inadimp = df_total[(df_total['score_interno'] <= 450) & (df_total['tempo_relacionamento_dias'] <= 120) & (df_total['num_emprestimos_anteriores'] == 0)&(df_total['inadimplente_90d'] == 1)]['valor_solicitado'].count()
loss_cliente_total = loss_client/count_clientes_geral
nova_inadimp = (count_clientes_inadim-loss_inadimp)/(count_clientes_geral-loss_client)
loss_recursos_inadimp = df_total[(df_total['score_interno'] <= 450) &(df_total['tempo_relacionamento_dias'] <= 120) & (df_total['num_emprestimos_anteriores'] == 0) & (df_total['inadimplente_90d'] == 1)]['valor_solicitado'].sum()
loss_recursos_total = df_total[(df_total['score_interno'] <= 450) & (df_total['tempo_relacionamento_dias'] <= 120) & (df_total['num_emprestimos_anteriores'] == 0)]['valor_solicitado'].sum()

print("Nova inadimplência:",(100*nova_inadimp).round(2),"%"),
print("Recuo da inadimplencia:",(100*(1-(nova_inadimp/tx_inadimplencia_geral))).round(2),"%"),
print("Recuo da carteira de clientes:",(100*loss_cliente_total).round(2),"%"),
print("Recuo da disponiblização de recursos:",(100*(loss_recursos_total/sum_recursos_total)).round(2),"%"),


## DENTRO DO GRUPO DE CLIENTES QUE NUNCA SOLICITARAM EMPRESTIMOS ANTERIORES E POSSUEM SCORE INTERNO DE 0 A 450
## NEGAR EMPRESTIMO A QUEM POSSUI MENOS DE 450 PONTOS DE SCORE INTERNO
## E POSSUA MENOS DE 120 DIAS DE RELACIONAMENTO COM A EMPRESA
## REDUZ A INADIMPLÊNCIA DE 18,10% PARA EM 15,75%
## MAS REPRESENTA UMA PERDA DE 11% NA CARTEIRA DE CLIENTES
## E RETRAÇÃO DE 11,10% NOS RECURSOS SOLICITADOS (R$ 883.800,00)

#%%

## ANALISE DE INADIMPLENCIA PELO CANAL DE AQUISIÇÃO

cross_canal_aquisicao_faixa_renda = pd.crosstab(
    df_total['canal_aquisicao'],
    df_total['faixa_comprometimento_renda']
)

cross_canal_aquisicao_faixa_renda_inadimplencia = pd.crosstab(
    df_inadimplencia['canal_aquisicao'],
    df_inadimplencia['faixa_comprometimento_renda']
)

cross_inadimp_total = (cross_canal_aquisicao_faixa_renda_inadimplencia)**3/cross_canal_aquisicao_faixa_renda

sns.heatmap(cross_inadimp_total, annot=True, cmap='coolwarm')

plt.show()



#%%
loss_client = cross_canal_aquisicao_faixa_renda.iloc[4,1]+cross_canal_aquisicao_faixa_renda.iloc[4,0]
loss_inadimp = cross_canal_aquisicao_faixa_renda_inadimplencia.iloc[4,1]+cross_canal_aquisicao_faixa_renda_inadimplencia.iloc[4,0]
loss_cliente_total = loss_client/count_clientes_geral
nova_inadimp = (count_clientes_inadim-loss_inadimp)/(count_clientes_geral-loss_client)
loss_recursos_inadimp = df_total[(df_total['canal_aquisicao'] =='Parceiro Marketplace B') &  (df_total['comprometimento_renda'] <=20)& (df_total['inadimplente_90d']==1)]['valor_solicitado'].sum()
loss_recursos_total = df_total[(df_total['canal_aquisicao'] =='Parceiro Marketplace B') &  (df_total['comprometimento_renda'] <=20)]['valor_solicitado'].sum().sum()

print("Nova inadimplência:",(100*nova_inadimp).round(2),"%"),
print("Recuo da inadimplencia:",(100*(1-(nova_inadimp/tx_inadimplencia_geral))).round(2),"%"),
print("Recuo da carteira de clientes:",(100*loss_cliente_total).round(2),"%"),
print("Recuo da disponiblização de recursos:",(100*(loss_recursos_total/sum_recursos_total)).round(2),"%"),

# Limitando crédito pelo Marketplace B a quem tem até 20% de renda comprometida
# Nova inadimplência: 17.33  %
# Recuo da inadimplencia: 4.27 %
# Recuo da carteira de clientes: 5.7 %
# Recuo da disponiblização de recursos: 4.02 %

#%%
## PRIORIDADE 1 - ACIMA DE 22% - RISCO ALTO

df_prob[df_prob['tx_inadimplencia'] >= 22]

#%%

## verificação de comprometimento de renda - 30 a 50

pd_cross = 100*pd.crosstab(
    df_inadimplencia['faixa_comprometimento_renda'],
    df_inadimplencia['faixa_renda_mensal'],
    normalize='all'
)
pd_cross.round(2)

## QUEM COMPROMETE DE 30 A 50% DA RENDA E POSSUI (0,2000) DE RENDA
## REPRESENTA 21,99% DE TODA A INADIMPLENCIA

#%%
cross_comp_renda_rendamensal_total = pd.crosstab(
    df_total['faixa_renda_mensal'],
    df_total['faixa_comprometimento_renda']
)

cross_comp_renda_rendamensal_inadimplencia = pd.crosstab(
    df_inadimplencia['faixa_renda_mensal'],
    df_inadimplencia['faixa_comprometimento_renda']
)

cross_inadimp_total = (cross_comp_renda_rendamensal_inadimplencia)**3/cross_comp_renda_rendamensal_total

sns.heatmap(cross_inadimp_total, annot=True, cmap='coolwarm')

plt.show()
#%%
loss_client = cross_comp_renda_rendamensal_total.iloc[0, 3]
loss_inadimp = cross_comp_renda_rendamensal_inadimplencia.iloc[0, 3]
loss_cliente_total = loss_client/count_clientes_geral
nova_inadimp = (count_clientes_inadim-loss_inadimp)/(count_clientes_geral-loss_client)
#%%
loss_recursos_inadimp = df_total[(df_total['score_interno'] <= 450) &(df_total['tempo_relacionamento_dias'] <= 120) & (df_total['num_emprestimos_anteriores'] == 0) & (df_total['inadimplente_90d'] == 1)]['valor_solicitado'].sum()
loss_recursos_inadimp
#%%
loss_recursos_total = df_total[(df_total['score_interno'] <= 450) & (df_total['tempo_relacionamento_dias'] <= 120) & (df_total['num_emprestimos_anteriores'] == 0)]['valor_solicitado'].sum()
loss_recursos_total

#%%

loss_recursos_inadimp,loss_recursos_total,loss_recursos_total/sum_recursos_total
#%%
nova_inadimp.round(4),loss_cliente_total,loss_recursos_inadimp,loss_recursos_total,loss_recursos_total/sum_recursos_total

## LIMITANDO CRÉDITO A QUEM COMPROMETE DE 30 A 50% DA RENDA 
## E POSSUI (0,2000) DE RENDA
## DIMINUI A INADIMPLENCIA DE 18,10% PARA APENAS 16,79%
## DIMINUI A CARTEIRA EM 15,88%
## DIMINUI A OFERTA DE CREDITO EM 11,10% 

#%%

## VERIFICAÇÃO DOS MESES 08-09-11 DE 2023

cross_inadimplencia = pd.crosstab(
    df_inadimplencia['data_contratacao'],
    df_inadimplencia['regiao'],
    normalize='all'
).round(4)

cross_total = pd.crosstab(
    df_total['data_contratacao'],
    df_total['regiao'],
    normalize='all'
).round(4)

cross = (cross_inadimplencia/cross_total)**10

sns.heatmap(cross, annot=True, cmap='coolwarm')

plt.show()

# inadimplencia veio do centrooeste no periodo - AGOSTO

#%%
cross_inadimplencia = pd.crosstab(
    df_inadimplencia['data_contratacao'],
    df_inadimplencia['faixa_renda_mensal'],
    normalize='all'
).round(4)

cross_total = pd.crosstab(
    df_total['data_contratacao'],
    df_total['faixa_renda_mensal'],
    normalize='all'
).round(4)

cross = (cross_inadimplencia/cross_total)**10


sns.heatmap(cross, annot=True, cmap='coolwarm')

plt.show()
## em setembro muito acentuado para maiores rendas - 5,5

#%%
cross_inadimplencia = pd.crosstab(
    df_inadimplencia['data_contratacao'],
    df_inadimplencia['canal_aquisicao'],
    normalize='all'
).round(4)

cross_total = pd.crosstab(
    df_total['data_contratacao'],
    df_total['canal_aquisicao'],
    normalize='all'
).round(4)

cross = (cross_inadimplencia/cross_total)**10


sns.heatmap(cross, annot=True, cmap='coolwarm')

plt.show()

# MÊS 11 - MARKETPLACE B
#%%
cross_inadimplencia = pd.crosstab(
    df_inadimplencia['data_contratacao'],
    df_inadimplencia['faixa_valor_solicitado'],
    normalize='all'
).round(4)

cross_total = pd.crosstab(
    df_total['data_contratacao'],
    df_total['faixa_valor_solicitado'],
    normalize='all'
).round(4)

cross = (cross_inadimplencia/cross_total)**10


sns.heatmap(cross, annot=True, cmap='coolwarm')

plt.show()

## mes 08 - 0 a 400
## mes 09 - 400 a 800

#%%

cross_inadimplencia = pd.crosstab(
    df_inadimplencia['data_contratacao'],
    df_inadimplencia['prazo_meses'],
    normalize='all'
).round(4)

cross_total = pd.crosstab(
    df_total['data_contratacao'],
    df_total['prazo_meses'],
    normalize='all'
).round(4)

cross = (cross_inadimplencia/cross_total)**10


sns.heatmap(cross, annot=True, cmap='coolwarm')


plt.show()

# MES 09 - PRAZO 3 MESES

#%%

# AGOSTO - CENTRO OESTE/VALOR SOLICITADO ATÉ 400 REAIS
# SETEMBRO - 3 PARCELAS/MAIORES RENDAS/400 A 800 REAIS
# NOVEMBRO - MARKETPLACE B

df_1 = df_total[(df_total['data_contratacao'] == '2023-08')&((df_total['regiao'] == 'Centro-Oeste')|((df_total['faixa_valor_solicitado'] == '(0,400]')))].describe()
## 40% inadimplencia
df_2 = df_total[(df_total['data_contratacao'] == '2023-09')&((df_total['prazo_meses'] == 3)|((df_total['faixa_renda_mensal'] == '(5000,600]')))].describe()
## 31,67% de inadimplencia
df_3 = df_total[(df_total['data_contratacao'] == '2023-11')&(df_total['canal_aquisicao'] == 'Parceiro Marketplace B')].describe()
## 54,54% de inadimplencia
df_2
#%%

df_total = df[[
    "id_cliente",        
    "data_contratacao",
    "idade",
    'faixa_idade',
    'sexo',
    'regiao',
    "renda_mensal",
    'faixa_renda_mensal',
    'classe_social',
    "score_interno",
    'faixa_score_interno',
    'canal_aquisicao',
    "num_emprestimos_anteriores",
    "tempo_relacionamento_dias",
    "faixa_tempo_relacionamento_dias",
    "valor_solicitado",
    'faixa_valor_solicitado',
    'possui_restricao',
    "prazo_meses",
    "taxa_juros_am",
    'faixa_taxa_juros_am',
    "valor_parcela",
    'faixa_valor_parcela',
    "comprometimento_renda",
    "faixa_comprometimento_renda",
    'finalidade',
    'dias_atraso_max',
    'faixa_dias_atraso_max',
    'status',
    'inadimplente_90d',
    ]]
#%%



#%%
pd.crosstab(
    df_total['faixa_score_interno'],
    df_total['inadimplente_90d'],
    normalize='index'
)

#%%

df_total.agg({
    'idade':['mean','std','max','min','median'],
    'renda_mensal':['mean','std','max','min','median'],
    'score_interno':['mean','std','max','min','median'],
})

#%%

df_total.quantile(0.25, numeric_only=True)

#%%

df_total.corr(numeric_only=True)['inadimplente_90d'].sort_values(ascending=False)