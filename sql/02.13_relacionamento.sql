WITH t1 AS (
    
    SELECT  
        CASE 
            WHEN tempo_relacionamento_dias <= 120 THEN 'Até 120 dias'
            WHEN tempo_relacionamento_dias > 120 and tempo_relacionamento_dias <= 240 THEN 'De 121 a 240 dias'
            WHEN tempo_relacionamento_dias > 240 and tempo_relacionamento_dias <= 360 THEN 'De 241 a 360 dias'
            WHEN tempo_relacionamento_dias > 360 and tempo_relacionamento_dias <= 480 THEN 'De 361 a 480 dias'
            WHEN tempo_relacionamento_dias > 480 and tempo_relacionamento_dias <= 520 THEN 'De 481 a 520 dias'
            ELSE 'Mais de 520 dias'
        END AS faixa_tempo_relacionamento,
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
    GROUP BY faixa_tempo_relacionamento

    ORDER BY faixa_tempo_relacionamento,percentual_inadimplentes DESC
)

SELECT faixa_tempo_relacionamento, total_valor_solicitado FROM t1