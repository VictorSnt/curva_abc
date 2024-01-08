current_stock_query = """
            SELECT DISTINCT ON (det.cdprincipal)
                es.qtestoque,
                det.cdprincipal
            FROM wshop.estoque AS es
            JOIN wshop.detalhe AS det ON det.iddetalhe = es.iddetalhe
            ORDER BY det.cdprincipal, es.dtreferencia DESC;

        """ 


get_idfamilia_query = """
SELECT idfamilia FROM wshop.detalhe
        WHERE cdprincipal = '{}' 
"""


similar_products_query = """
SELECT DISTINCT ON (det.dsdetalhe)
            det.dsdetalhe,
            es.qtestoque
        FROM wshop.estoque as es
        JOIN wshop.detalhe AS det ON det.iddetalhe = es.iddetalhe
        WHERE det.idfamilia = '{}'
        AND det.stdetalheativo = true 
        ORDER BY det.dsdetalhe, es.dtreferencia DESC    
"""



dsdetalhe_query = """
        SELECT dsdetalhe FROM wshop.detalhe
    """