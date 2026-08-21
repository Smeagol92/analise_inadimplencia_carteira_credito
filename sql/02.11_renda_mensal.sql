WITH t1 AS (
    
    SELECT  
        CASE 
            WHEN renda_mensal <= 1000 THEN 'Até R$ 1.000'
            WHEN renda_mensal > 1000 and renda_mensal <= 2000 THEN 'Entre R$ 1.001 e R$ 2.000'
            WHEN renda_mensal > 2000 and renda_mensal <= 3000 THEN 'Entre R$ 2.001 e R$ 3.000'
            WHEN renda_mensal > 3000 and renda_mensal <= 4000 THEN 'Entre R$ 3.001 e R$ 4.000'
            WHEN renda_mensal > 4000 and renda_mensal <= 5000 THEN 'Entre R$ 4.001 e R$ 5.000'
            ELSE 'Acima de R$ 5.000'
        END AS faixa_renda,
        COUNT(*) AS total_clientes,
        ROUND((COUNT(*) * 100.0 / SUM(COUNT(*)) OVER()), 2) AS percentual_clientes,
        ROUND(AVG(idade), 2) AS media_idade,
        ROUND(AVG(renda_mensal), 2) AS media_renda_mensal,
        ROUND(AVG(score_interno), 2) AS media_score_interno,
        ROUND(AVG(num_emprestimos_anteriores), 2) AS media_num_emprestimos_anteriores,
        ROUND(AVG(tempo_relacionamento_dias), 2) AS media_tempo_relacionamento,
        sum(possui_restricao) AS total_clientes_restricao,
        ROUND(AVG(valor_solicitado), 2) AS media_valor_solicitado,
        sum(valor_solicitado) AS total_valor_solicitado,
        ROUND(AVG(prazo_meses), 2) AS media_prazo_meses,
        ROUND(AVG(taxa_juros_am), 2) AS media_taxa_juros_am,
        ROUND(AVG(valor_parcela), 2) AS media_valor_parcela,
        ROUND(AVG(comprometimento_renda), 2) AS media_comprometimento_renda,
        ROUND(AVG(dias_atraso_max), 2) AS media_dias_atraso_max,
        sum(inadimplente_90d) AS total_inadimplentes,
        ROUND((sum(inadimplente_90d) * 100.0 / count(id_cliente)), 2) AS percentual_inadimplentes  

    FROM case_inadimplencia_dataset
    WHERE inadimplente_90d = 1
    GROUP BY faixa_renda

    ORDER BY percentual_inadimplentes DESC
)

SELECT faixa_renda, total_valor_solicitado FROM t1