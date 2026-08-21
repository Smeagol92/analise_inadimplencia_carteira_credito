WITH t1 AS (
    
    SELECT  
        CASE 
            WHEN valor_parcela <= 200 THEN 'Até 200'
            WHEN valor_parcela > 200 and valor_parcela <= 300 THEN 'De 201 a 300'
            WHEN valor_parcela > 300 and valor_parcela <= 400 THEN 'De 301 a 400'
            WHEN valor_parcela > 400 and valor_parcela <= 500 THEN 'De 401 a 500'
            WHEN valor_parcela > 500 and valor_parcela <= 750 THEN 'De 501 a 750'
            ELSE 'Mais de 750'
        END AS faixa_valor_parcela,
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
    GROUP BY faixa_valor_parcela

    ORDER BY faixa_valor_parcela,percentual_inadimplentes DESC
)

SELECT faixa_valor_parcela, total_valor_solicitado FROM t1