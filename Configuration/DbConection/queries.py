current_stock_query = """
            SELECT qtestoque, cdprincipal
            FROM (
                SELECT es.qtestoque, det.cdprincipal,
                    ROW_NUMBER() OVER (PARTITION BY det.cdprincipal ORDER BY es.dtreferencia DESC) AS rn
                FROM wshop.estoque AS es
                JOIN wshop.detalhe AS det ON det.iddetalhe = es.iddetalhe
            ) subquery
            WHERE rn = 1;
        """ 