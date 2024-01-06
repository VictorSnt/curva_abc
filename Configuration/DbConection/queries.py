current_stock_query = """
            SELECT DISTINCT ON (det.cdprincipal)
                es.qtestoque,
                det.cdprincipal
            FROM wshop.estoque AS es
            JOIN wshop.detalhe AS det ON det.iddetalhe = es.iddetalhe
            ORDER BY det.cdprincipal, es.dtreferencia DESC;

        """ 

dsdetalhe_query = """
        SELECT dsdetalhe FROM wshop.detalhe
    """