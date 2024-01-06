from pathlib import Path
import xlrd


def importar_xls(xml_file_path):
    
    try:
        xml_file_path = Path(xml_file_path)
        workbook = xlrd.open_workbook(xml_file_path)
        sheet = workbook.sheet_by_index(0)

        lista_de_listas = []

        for row_index in range(sheet.nrows):
            linha = [sheet.cell_value(row_index, col) for col in range(sheet.ncols)]
            lista_de_listas.append(linha)

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
        print(f"Erro ao importar o arquivo XLS: {e}")
        return None

    finally:
        
        if xml_file_path.exists():
            xml_file_path.unlink()