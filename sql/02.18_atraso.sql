WITH t1 AS (
    
    SELECT  
        CASE 
            WHEN dias_atraso_max <= 45 THEN 'De 0 a 45 dias'
            WHEN dias_atraso_max > 45 and dias_atraso_max <= 90 THEN 'De 46 a 90 dias'
            WHEN dias_atraso_max > 90 and dias_atraso_max <= 135 THEN 'De 91 a 135 dias'
            WHEN dias_atraso_max > 135 and dias_atraso_max <= 180 THEN 'De 136 a 180 dias'
            WHEN dias_atraso_max > 180 and dias_atraso_max <= 225 THEN 'De 181 a 225 dias'
            ELSE 'Mais de 225 dias'
        END AS faixa_dias_atraso,
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
    GROUP BY faixa_dias_atraso

    ORDER BY faixa_dias_atraso
)

SELECT faixa_dias_atraso, total_valor_solicitado FROM t1