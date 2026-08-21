WITH t1 AS (
    
    SELECT  
        CASE 
            WHEN valor_solicitado <= 400 THEN 'Até 400'
            WHEN valor_solicitado > 400 and valor_solicitado <= 800 THEN 'De 401 a 800'
            WHEN valor_solicitado > 800 and valor_solicitado <= 1200 THEN 'De 801 a 1200'
            WHEN valor_solicitado > 1200 and valor_solicitado <= 1600 THEN 'De 1201 a 1600'
            WHEN valor_solicitado > 1600 and valor_solicitado <= 2000 THEN 'De 1601 a 2000'
            WHEN valor_solicitado > 2000 and valor_solicitado <= 2400 THEN 'De 2001 a 2400'
            WHEN valor_solicitado > 2400 and valor_solicitado <= 3200 THEN 'De 2401 a 3200'
            ELSE 'Mais de 3200'
        END AS faixa_valor_solicitado,
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
    GROUP BY faixa_valor_solicitado

    ORDER BY faixa_valor_solicitado,percentual_inadimplentes DESC
)

SELECT faixa_valor_solicitado, total_valor_solicitado FROM t1