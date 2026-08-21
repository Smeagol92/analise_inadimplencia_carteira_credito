SELECT  
    CASE 
        WHEN  inadimplente_90d = 1 THEN 'Inadimplente'
        ELSE 'Adimplente'
    END AS status_inadimplencia,
    COUNT(*),
    ROUND((COUNT(*) * 100.0 / SUM(COUNT(*)) OVER()), 3) AS percentual_clientes,
    ROUND(AVG(idade), 3) AS media_idade,
    ROUND(AVG(renda_mensal), 3) AS media_renda_mensal,
    ROUND(AVG(score_interno), 3) AS media_score_interno,
    ROUND(AVG(num_emprestimos_anteriores), 3) AS media_num_emprestimos_anteriores,
    ROUND(AVG(tempo_relacionamento_dias), 3) AS media_tempo_relacionamento,
    sum(possui_restricao) AS total_clientes_restricao,
    ROUND(AVG(valor_solicitado), 3) AS media_valor_solicitado,
    sum(valor_solicitado) AS total_valor_solicitado,
    ROUND(AVG(prazo_meses), 3) AS media_prazo_meses,
    ROUND(AVG(taxa_juros_am), 3) AS media_taxa_juros_am,
    ROUND(AVG(valor_parcela), 3) AS media_valor_parcela,
    ROUND(AVG(comprometimento_renda), 3) AS media_comprometimento_renda,
    ROUND(AVG(dias_atraso_max), 3) AS media_dias_atraso_max,
    sum(inadimplente_90d) AS total_inadimplentes,
    ROUND((sum(inadimplente_90d) * 100.0 / count(id_cliente)), 3) AS percentual_inadimplentes

FROM case_inadimplencia_dataset

GROUP BY status_inadimplencia
