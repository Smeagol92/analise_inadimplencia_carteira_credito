#%%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns    

# =========================
# CONFIGURAÇÕES
# =========================
df = pd.read_csv("C:/Users/Francisco/Desktop/case_enova/case_inadimplencia_dataset.csv")

# =========================
# PREPARAÇÃO
# =========================

def prepare_data(df):
    df = df.copy()

    df['data_contratacao'] = pd.to_datetime(
          df['data_contratacao']).dt.to_period('M')

    df['taxa_juros_am'] = 100.00*df['taxa_juros_am']

    df['comprometimento_renda'] = 100.00*df['comprometimento_renda']

    df['faixa_idade'] = pd.cut(
          df['idade'],
          bins=[0,20,30,40,50,60,70]
    )

    df['faixa_renda_mensal'] = pd.cut(
          df['renda_mensal'],
          bins=[0,1000,2000,3000,4000,5000,6000]
    )

    df['faixa_score_interno'] = pd.cut(
          df['score_interno'],
          bins=[0,150,300,450,600,750,1000]
    )
        
    df['faixa_tempo_relacionamento_dias'] = pd.cut(
          df['tempo_relacionamento_dias'],
          bins=[0,120,240,360,480,600,720,840,960]
    )

    df['faixa_valor_solicitado'] = pd.cut(
          df['valor_solicitado'],
          bins=[0,400,800,1200,1600,2000,2400,2800,3200]
    )

    df['faixa_taxa_juros_am'] = pd.cut(
          df['taxa_juros_am'],
          bins=[3,6,9,12,15,18]
    )

    df['faixa_valor_parcela'] = pd.cut(
            df['valor_parcela'],
                bins=[0,200,400,600,800,1000,1200,1400]
        )

    df['faixa_comprometimento_renda'] = pd.cut(
          df['comprometimento_renda'],
          bins=[0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150]
    )

    df['faixa_dias_atraso_max'] = pd.cut(
          df['dias_atraso_max'], 
          bins=(0, 45, 90, 135, 180, 225, 270), 
          include_lowest=True
    )

    df['status'] = df['inadimplente_90d'].map(
          {1: 'inadimplente', 0: 'adimplente'}
    )
    return df

df = prepare_data(df)

#%%
# =========================
# FUNÇÕES DE ANÁLISE
# =========================

def calculate_portfolio_metrics(df):

    total_clients = df["inadimplente_90d"].count()

    default_clients = df["inadimplente_90d"].sum()

    default_rate = (
        default_clients / total_clients
    )

    total_requested = df["valor_solicitado"].sum()

    default_requested = df.loc[
        df["inadimplente_90d"] == 1,
        "valor_solicitado"
    ].sum()

    return {
        "total_clients": total_clients,
        "default_clients": default_clients,
        "default_rate": default_rate,
        "total_requested": total_requested,
        "default_requested": default_requested,
    }

def default_rate_by_category(df, column):

    result = (
        df.groupby(column, observed=True)
        .agg(
            default_rate=("inadimplente_90d", "mean"),

            clients=("inadimplente_90d", "size")
        )
        .reset_index()
    )

    result["portfolio_share"] = (
        result["clients"] / len(df)
    )

    return result.sort_values(
        "default_rate",
        ascending=False
    )

def simulate_strategy(df, filter_condition):

    affected_clients = df[filter_condition]

    affected_defaults = affected_clients[
        affected_clients["inadimplente_90d"] == 1
    ]

    new_df = df.loc[~filter_condition]

    original_default_rate = df["inadimplente_90d"].mean()

    new_default_rate = new_df["inadimplente_90d"].mean()

    default_reduction = (
        original_default_rate - new_default_rate
        )

    

    return {
        "affected_clients": len(affected_clients),
        "affected_defaults": len(affected_defaults),
        "new_default_rate": 100*new_df["inadimplente_90d"].mean(),
        "default_rate_reduction": 100*default_reduction,
        "portfolio_reduction": (
            100*(len(affected_clients) / len(df))
        ),
        "credit_reduction": (
            100*(affected_clients["valor_solicitado"].sum()
            / df["valor_solicitado"].sum())
        )
    }

# =========================
# ANÁLISE
# =========================

date_analysis = default_rate_by_category(
    df,
    "data_contratacao"
)
age_analysis = default_rate_by_category(
    df,
    "faixa_idade"
)
gender_analysis = default_rate_by_category(
    df,
    "sexo"
)
region_analysis = default_rate_by_category(
    df,
    "regiao"
)
income_analysis = default_rate_by_category(
    df,
    "faixa_renda_mensal"
)
class_analysis = default_rate_by_category(
    df,
    "classe_social"
)
score_analysis = default_rate_by_category(
    df,
    "faixa_score_interno"
)
channel_analysis = default_rate_by_category(
    df,
    "canal_aquisicao"
)
previous_loans_analysis = default_rate_by_category(
    df,
    "num_emprestimos_anteriores"
)
number_of_installments_analysis = default_rate_by_category(
    df,
    "prazo_meses"
)
goal_analysis = default_rate_by_category(
    df,
    "finalidade"
)
relationship_time_analysis = default_rate_by_category(
    df,
    "faixa_tempo_relacionamento_dias"
)
requested_amount_analysis = default_rate_by_category(
    df,
    "faixa_valor_solicitado"
)
interest_rate_analysis = default_rate_by_category(
    df,
    "faixa_taxa_juros_am"
)
installment_amount_analysis = default_rate_by_category(
    df,
    "faixa_valor_parcela"
)
borrowing_percentege_analysis = default_rate_by_category(
    df,
    "faixa_comprometimento_renda"
)

df_inadimplencia = df[df["inadimplente_90d"] == 1]
#%%

df.groupby('faixa_score_interno').agg({
    'renda_mensal':['mean','std','max','min','median'],
    'tempo_relacionamento_dias':['mean','std','max','min','median'],
    'inadimplente_90d':['mean']
}).round(3).T
#%%
cross_restricao_valor_solicitado = pd.crosstab(
    df_inadimplencia['faixa_score_interno'],
    df_inadimplencia['faixa_tempo_relacionamento_dias'],
    normalize='all'
)

sns.heatmap(cross_restricao_valor_solicitado, annot=True, cmap='coolwarm')

plt.show()
#%%

cross_restricao_valor_solicitado = pd.crosstab(
    df_inadimplencia['faixa_score_interno'],
    df_inadimplencia['num_emprestimos_anteriores'],
    normalize='all'
)

sns.heatmap(cross_restricao_valor_solicitado, annot=True, cmap='coolwarm')

plt.show()
#%%

condition = (
    (df["score_interno"] <= 450)
    & (df["tempo_relacionamento_dias"] <= 120)
    & (df["num_emprestimos_anteriores"] == 0)
)

result = simulate_strategy(df, condition)
result

#%%

## CLIENTES QUE POSSUAM RESTRIÇÃO

df.groupby(['possui_restricao']).agg({
    'valor_solicitado':['mean','median'],
    'inadimplente_90d':['mean']
}).round(2).T
#%%
cross_restricao_valor_solicitado = pd.crosstab(
    df_inadimplencia['possui_restricao'],
    df_inadimplencia['faixa_valor_solicitado'],
    normalize='columns'
)

sns.heatmap(cross_restricao_valor_solicitado, annot=True, cmap='coolwarm')

plt.show()
#%%

condition = (
    (df["possui_restricao"] == 1)
    & (df["valor_solicitado"] > 2800)
)

result = simulate_strategy(df, condition)
result

#%%
## ANALISE DE INADIMPLENCIA PELO NUMERO DE EMPRESTIMOS ANTERIORES

df_inadimplencia.groupby('num_emprestimos_anteriores').agg({
    'id_cliente':['count'],
    'score_interno':['mean','std','max','min','median'],
    'tempo_relacionamento_dias':['mean','std','max','min','median']
}).round(3).T

#%%
cross_emp_anteriores_score_inadimplencia = pd.crosstab(
    df_inadimplencia['num_emprestimos_anteriores'],
    df_inadimplencia['faixa_score_interno'],
    normalize='all'
)

sns.heatmap(cross_emp_anteriores_score_inadimplencia, annot=True, cmap='coolwarm')

plt.show()
#%%

condition = (
    (df["num_emprestimos_anteriores"] == 0)
    & (df["score_interno"] <450)
)

result = simulate_strategy(df, condition)
result

#%%

cross_comp_renda_rendamensal_inadimplencia = pd.crosstab(
    df_inadimplencia['faixa_renda_mensal'],
    df_inadimplencia['faixa_comprometimento_renda'],
    normalize='columns'
)

sns.heatmap(cross_comp_renda_rendamensal_inadimplencia, annot=True, cmap='coolwarm')

plt.show()

#%%

condition = (
    (df["renda_mensal"] <= 1000)
    & (df["comprometimento_renda"] >1)
)

result = simulate_strategy(df, condition)
result
#%%

# =========================
# ESTRATÉGIAS
# =========================

strategies = {
    "baixo_score_pouco_relacionamento": (
        (df["score_interno"] <= 450)
        & (df["tempo_relacionamento_dias"] <= 120)
        & (df["num_emprestimos_anteriores"] == 0)
    ),

    "marketplace_b_comprometimento_alto": (
        (df["canal_aquisicao"] == "Parceiro Marketplace B")
        & (df["comprometimento_renda"] > 20)
    ),

    "retricao_valor2800+":(
            (df["possui_restricao"] == 1)
            & (df["valor_solicitado"] > 2800)
    ),

    "sem_emprestimo_anterior_score450-":(
    (df["num_emprestimos_anteriores"] == 0)
    & (df["score_interno"] <450)
    ),

    "renda1000-_comp_renda100+":(
    (df["renda_mensal"] <= 1000)
    & (df["comprometimento_renda"] >100)
    )

}
results = []

for name, condition in strategies.items():

    result = simulate_strategy(df, condition)
    result["strategy"] = name

    results.append(result)

strategy_results = pd.DataFrame(results)

strategy_results
