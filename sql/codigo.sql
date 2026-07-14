-- INSERÇÃO DE COLUNAS QUE REPRESENTAM FAIXAS DE VARIÁVEIS NUMÉRICAS 
-- (IDADE, RENDA, SCORE, TEMPO DE RELACIONAMENTO, VALOR SOLICITADO, 
-- TAXA DE JUROS, VALOR PARCELA, COMPROMETIMENTO DE RENDA 
-- E DIAS DE ATRASO) PARA ANÁLISE DE INADIMPLÊNCIA.

-- tabela_base_tratada: CASO NECESSÁRIA CONSULTA NÃO PREVISTA EM tabela_panorama_grupos

WITH tabela_base_tratada AS (
        
        SELECT  id_cliente,
                data_contratacao,
                STRFTIME('%Y-%m', data_contratacao) AS mes_ano_contratacao,
                idade,
                CASE 
                    WHEN idade <= 20 THEN '0-20'
                    WHEN idade > 20 and idade <= 30 THEN '21-30'
                    WHEN idade > 30 and idade <= 40 THEN '31-40'
                    WHEN idade > 40 and idade <= 50 THEN '41-50'
                    WHEN idade > 50 and idade <= 60 THEN '51-60'
                    ELSE '60+' 
                END AS faixa_idade,
                sexo,
                regiao,
                renda_mensal,
                CASE 
                    WHEN renda_mensal <= 1000 THEN 'R$ 0.00 - 1.000'
                    WHEN renda_mensal > 1000 and renda_mensal <= 2000 THEN 'R$ 1.001 - 2.000'
                    WHEN renda_mensal > 2000 and renda_mensal <= 3000 THEN 'R$ 2.001 - 3.000'
                    WHEN renda_mensal > 3000 and renda_mensal <= 4000 THEN 'R$ 3.001 - 4.000'
                    WHEN renda_mensal > 4000 and renda_mensal <= 5000 THEN 'R$ 4.001 - 5.000'
                    ELSE 'R$ 5.000+'
                END AS faixa_renda,
                classe_social,
                score_interno,
                CASE 
                    WHEN score_interno <= 150 THEN '0-150'
                    WHEN score_interno > 150 and score_interno <= 300 THEN '151-300'
                    WHEN score_interno > 300 and score_interno <= 450 THEN '301-450'
                    WHEN score_interno > 450 and score_interno <= 600 THEN '451-600'
                    WHEN score_interno > 600 and score_interno <= 750 THEN '601-750'
                    ELSE '750+'
                END AS faixa_score,
                canal_aquisicao,
                num_emprestimos_anteriores,
                tempo_relacionamento_dias,
                CASE 
                    WHEN tempo_relacionamento_dias <= 120 THEN '0-120'
                    WHEN tempo_relacionamento_dias > 120 and tempo_relacionamento_dias <= 240 THEN '121-240'
                    WHEN tempo_relacionamento_dias > 240 and tempo_relacionamento_dias <= 360 THEN '241-360'
                    WHEN tempo_relacionamento_dias > 360 and tempo_relacionamento_dias <= 480 THEN '361-480'
                    WHEN tempo_relacionamento_dias > 480 and tempo_relacionamento_dias <= 520 THEN '481-520'
                    ELSE '520+'
                END AS faixa_tempo_relacionamento,
                possui_restricao,
                valor_solicitado,
                CASE 
                    WHEN valor_solicitado <= 400 THEN '0-400'
                    WHEN valor_solicitado > 400 and valor_solicitado <= 800 THEN '401-800'
                    WHEN valor_solicitado > 800 and valor_solicitado <= 1200 THEN '801-1200'
                    WHEN valor_solicitado > 1200 and valor_solicitado <= 1600 THEN '1201-1600'
                    WHEN valor_solicitado > 1600 and valor_solicitado <= 2000 THEN '1601-2000'
                    WHEN valor_solicitado > 2000 and valor_solicitado <= 2400 THEN '2001-2400'
                    WHEN valor_solicitado > 2400 and valor_solicitado <= 3200 THEN '2401-3200'
                    ELSE '>3200'
                END AS faixa_valor_solicitado,
                prazo_meses,
                taxa_juros_am,
                CASE 
                    WHEN taxa_juros_am <= 0.09 THEN '0 - 9%'
                    WHEN taxa_juros_am > 0.09 and taxa_juros_am <= 0.12 THEN '9 - 12%'
                    WHEN taxa_juros_am > 0.12 and taxa_juros_am <= 0.15 THEN '12 - 15%'
                    ELSE '>15%'
                END AS faixa_taxa_juros,
                valor_parcela,
                CASE 
                    WHEN valor_parcela <= 200 THEN 'Até 200'
                    WHEN valor_parcela > 200 and valor_parcela <= 300 THEN '201 - 300'
                    WHEN valor_parcela > 300 and valor_parcela <= 400 THEN '301 - 400'
                    WHEN valor_parcela > 400 and valor_parcela <= 500 THEN '401 - 500'
                    WHEN valor_parcela > 500 and valor_parcela <= 750 THEN '501 - 750'
                    ELSE '>750'
                END AS faixa_valor_parcela,
                comprometimento_renda,
                CASE 
                    WHEN comprometimento_renda <= .10 THEN '0 - 10%'
                    WHEN comprometimento_renda > .10 and comprometimento_renda <= .20 THEN '10 - 20%'
                    WHEN comprometimento_renda > .20 and comprometimento_renda <= .30 THEN '20 - 30%'
                    WHEN comprometimento_renda > .30 and comprometimento_renda <= .40 THEN '30 - 40%'
                    ELSE '>40%'
                END AS faixa_comprometimento_renda,
                finalidade,
                dias_atraso_max,
                CASE 
                    WHEN dias_atraso_max <= 89 THEN '0 - 89 dias'
                    WHEN dias_atraso_max > 89 and dias_atraso_max <= 135 THEN '90 - 135 dias'
                    WHEN dias_atraso_max > 135 and dias_atraso_max <= 180 THEN '136 - 180 dias'
                    WHEN dias_atraso_max > 180 and dias_atraso_max <= 225 THEN '181 - 225 dias'
                    ELSE '>225 dias'
                END AS faixa_dias_atraso,
                inadimplente_90d

        FROM case_inadimplencia_dataset
),

-- tabela_panorama_grupos: VOLTADA PARA ANÁLISE DE SUBGRUPOS DA CARTEIRA

tabela_panorama_grupos AS(

    SELECT

    -- ALTERE APENAS UM TERMO ANTES DO "AS" NESTA LINHA PARA ANALISE 
    -- E CONSQUENTES FILTROS CASO NECESSÁRIO

    --          mes_ano_contratacao: '2023-07' A '2024-12'
    --          idade: VALOR INTEIRO
    --          faixa_idade: '0-20';'21-30';'31-40';'41-50';'51-60';'60+'
    --          sexo: 'M';'F;
    --          regiao: 'SUL';'SUDESTE';'CENTRO-OESTE'
    --          renda_mensal: QUALQUER NÚMERO POSITIVO
    --          faixa_renda: 'R$ 0.00 - 1.000';'R$ 1.001 - 2.000';'R$ 2.001 - 3.000';
    --          'R$ 3.001 - 4.000';'R$ 4.001 - 5.000';'R$ 5.000+'
    --          classe_social: 'C';'D'
    --          score_interno: QUALQUER NÚMERO POSITIVO
    --          faixa_score: '0-150';'151-300';'301-450';'451-600';'601-750';'750+'
    --          canal_aquisicao: 'Parceiro Marketplace A'; 'Parceiro Marketplace B'; 
    --          'Midia Paga'; 'Site'; 'App Proprio'; 'Indicação'
    --          num_emprestimos_anteriores: NUMERO INTEIRO POSITIVO MAIOR OU IGUAL A 0
    --          tempo_relacionamento_dias: NUMERO INTEIRO POSITIVO MAIOR OU IGUAL A 0
    --          faixa_tempo_relacionamento:'0-120';'121-240';'241-360';'361-480';'481-520';'520+'
    --          possui_restricao: 0 ou 1
    --          valor_solicitado: NUMERO POSITIVO
    --          faixa_valor_solicitado:'0-400';'401-800';'801-1200';'1201-1600';
    --          '1601-2000';'2001-2400';'2401-3200';'>3200'
    --          prazo_meses: 3, 6, 9, 12
    --          taxa_juros_am: NUMERO POSITIVO
    --          faixa_taxa_juros:'0 - 9%';'9 - 12%';'12 - 15%';'>15%'
    --          valor_parcela: NUMERO POSITIVO
    --          faixa_valor_parcela: 'Até 200';'201 - 300';'301 - 400';
    --          '401 - 500';'501 - 750'; '>750'
    --          comprometimento_renda: NUMERO POSITIVO
    --          faixa_comprometimento_renda: '0 - 10%'; '10 - 20%'; '20 - 30%'; '30 - 40%'; '>40%'
    --          finalidade: 'Pagar dívida'; 'Consumo', 'Saúde', 'Educação', 'Reforma', 'Emergência'
    --          dias_atraso_max: NUMERO POSITIVO
    --          faixa_dias_atraso: '0 - 45 dias'; '46 - 90 dias'; '91 - 135 dias'; '136 - 180 dias'
    --          '181 - 225 dias'; '>225 dias'
    --          inadimplente_90d: 0 ou 1    

    -- ==============================================================
    --  INSERIR SUBGRUPO ACIMAR CASO NECESSÁRIO    
        faixa_comprometimento_renda AS subgrupo,
    -- ==============================================================
        
        COUNT(*) AS total_clientes,
        ROUND((COUNT(*) * 100.0 / SUM(COUNT(*)) OVER()), 2) AS percentual_clientes,
        ROUND(AVG(idade),2) AS media_idade,
        ROUND(AVG(renda_mensal),2) AS media_renda_mensal,
        ROUND(AVG(score_interno),2) AS media_score_interno,
        ROUND(AVG(num_emprestimos_anteriores),2) AS media_num_emprestimos_anteriores,
        ROUND(AVG(tempo_relacionamento_dias),2) AS media_tempo_relacionamento,
        ROUND(AVG(valor_solicitado),2) AS media_valor_solicitado,
        SUM(valor_solicitado) AS soma_valor_solicitado,
        ROUND((SUM(valor_solicitado) * 100.0 / SUM(SUM(valor_solicitado)) OVER()), 2) AS percentual_valor_solicitado,
        ROUND(AVG(taxa_juros_am),2) AS media_taxa_juros_am,
        ROUND(AVG(valor_parcela),2) AS media_valor_parcela,
        ROUND(AVG(comprometimento_renda),2) AS media_comprometimento_renda,
        ROUND(AVG(dias_atraso_max),2) AS media_dias_atraso,
        SUM(inadimplente_90d) AS total_inadimplencia,
        ROUND((sum(inadimplente_90d) * 100.0 / count(*)), 2) AS percentual_inadimplentes

    FROM tabela_base_tratada

    -- ==============================================================
    -- FILTROS (OPCIONAL) DESCRITOS ACIMA
    WHERE valor_solicitado <1000
    -- INSERIR "GROUP BY SUBGRUPO" CASO HAJA INSERÇÃO DE SUBGRUPO ACIMA
    
    -- ==============================================================

    ORDER BY percentual_clientes DESC, percentual_inadimplentes DESC
)

SELECT * FROM tabela_panorama_grupos
