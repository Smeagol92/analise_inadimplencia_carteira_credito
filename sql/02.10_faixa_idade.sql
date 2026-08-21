WITH t1 AS (
    
    SELECT  
        CASE 
            WHEN idade <= 20 THEN 'Jovem de 0 a 20'
            WHEN idade > 20 and idade <= 30 THEN 'Entre 21 e 30'
            WHEN idade > 30 and idade <= 40 THEN 'Entre 31 e 40'
            WHEN idade > 40 and idade <= 50 THEN 'Entre 41 e 50'
            WHEN idade > 50 and idade <= 60 THEN 'Entre 51 e 60'
            ELSE 'Maior que 60' 
        END AS faixa_idade,
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
    where inadimplente_90d = 1
    GROUP BY faixa_idade

    ORDER BY percentual_inadimplentes DESC
)

SELECT faixa_idade, total_valor_solicitado FROM t1