from flask import Flask, redirect, render_template, request

from Configuration.DbConection.queries import current_stock_query
from util import importar_xls, connect_to_database

from json import dump, load
from pathlib import Path
import logging


app = Flask(__name__)
json_temp_path = Path(app.static_folder + '\\temp_json.json')
xls_temp_path = Path(app.static_folder + '\\abc.xls')

if not Path(app.static_folder).exists():
    Path(app.static_folder).mkdir()

logging.basicConfig(

    filename='app.log', 
    filemode='a', 
    format='%(asctime)s - %(message)s', 
    level=logging.ERROR,
    encoding='utf-8'
)


@app.get('/')
def index():
    try:
        return render_template("index.html")
    
    except Exception as e:
        logging.error("Exceção ocorrida", exc_info=True) 
        return render_template('error.html', error=str(e))

@app.post('/xls')
def get_xls():
    try:
        if 'xlsFile' not in request.files:
            raise FileNotFoundError("Nenhum arquivo enviado.")
        
        json_path = json_temp_path
        xls_path = xls_temp_path
        xls = request.files['xlsFile']
        xls.save(xls_path)
        data = importar_xls(xls_path)

        if not isinstance(data, list):
            raise ValueError(str(data))
        
        with open(json_path, 'w') as temp_json:
            dump(data, temp_json, indent=4)

        return redirect('/relatorio')

    except Exception as e:
        logging.error("Exceção ocorrida", exc_info=True) 
        return render_template('error.html', error=str(e))


@app.get('/relatorio')
def relatorio():
    try:
        json_path = json_temp_path
        if not Path(json_path).exists():
            raise FileNotFoundError
        
        with open(json_path, 'r') as json_file:
            datas = load(json_file)
        
        if not isinstance(datas, list):
            raise ValueError('data should be a list') 
        
        if len(datas) < 1:
            raise ValueError('your spreadsheet is empty')
        
        db_conn = connect_to_database()
        response = db_conn.sqlquery(current_stock_query)
      
        if not response:
            raise ValueError('response should not be None')

        db_conn.closeconnection()

        stock_quants: dict = {
            res['cdprincipal']: res['qtestoque'] for res in response
        }

        result = []
        for data in datas:  

            cdprincipal = data['cdprincipal']
            data['qtestoque'] = stock_quants.get(cdprincipal)
            result.append(data)

        result_abc = sorted(result, key=lambda x: x['abcrank'])

        return render_template('report.html', result_abc=result_abc)
    
    except Exception as e:
        logging.error("Exceção ocorrida", exc_info=True) 
        return render_template('error.html', error=str(e))
    
if __name__ == '__main__':
    app.run()
