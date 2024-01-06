import xlrd

from Configuration.DbConection.DbConnect import DbConnection
from Configuration.DbConection.queries import dsdetalhe_query

from pathlib import Path
from dotenv import load_dotenv
from os import environ

def importar_xls(xml_file_path):
    
    try:
        xml_file_path = Path(xml_file_path)
        workbook = xlrd.open_workbook(xml_file_path)
        sheet = workbook.sheet_by_index(0)

        lista_de_listas: list[list[str|float]] = []

        for row_index in range(sheet.nrows):
            linha = [sheet.cell_value(row_index, col) for col in range(sheet.ncols)]
            lista_de_listas.append(linha)
        
        if not lista_de_listas:
            return "Seu relatorio esta vazio"

        if not sheet_validator(lista_de_listas):
            return "O formato do relatorio parece incorreto!"
        
        dados = [
            {
                'cdprincipal': data[0], 
                "dsdetalhe": data[1], 
                'qtvenda': data[2], 
                'abcrank': data[-4]
                
            }for data in lista_de_listas
        ]
        
        return dados

    except Exception as e:
        return e

    finally:
        
        if xml_file_path.exists():
            xml_file_path.unlink()
        

def connect_to_database() -> DbConnection:

    load_dotenv()
    
    db_conn = DbConnection(
        
        environ['HOST'], 
        environ['PORT'], 
        environ['DBNAME'], 
        environ['USER'], 
        environ['PASSWD']
    )
    
    if not db_conn.connect():
        raise db_conn.error
    
    return db_conn 
        
def sheet_validator(lista_de_listas: list[list[str|float]]):
    

    is_cdprincipal_valid = [True for data in lista_de_listas if (
        data[0].isnumeric()
    )]
    is_cdprincipal_valid = all(is_cdprincipal_valid)
    
    conn = connect_to_database()
    
    result = conn.sqlquery(dsdetalhe_query)
    
    if not result:
        return False
    descriptions = [ds['dsdetalhe'] for ds in result]
    descriptions_dict = {ds: True for ds in descriptions}

    is_dsdetalhe_valid = [
       descriptions_dict.get(data[1], False) 
       for data in lista_de_listas
    ]

    is_dsdetalhe_valid = all(is_dsdetalhe_valid)

    is_qtvenda_valid = all(
        isinstance(data[2], float)
        for data in lista_de_listas
    )
   
    is_abcrank_valid = all(
        data[-4] in ['A', 'B', 'C'] for data in lista_de_listas
    )
    
    return all(

        [is_abcrank_valid, 
        is_cdprincipal_valid, is_dsdetalhe_valid, 
        is_qtvenda_valid]
    )