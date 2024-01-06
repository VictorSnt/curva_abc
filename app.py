import re
from flask import Flask, redirect, render_template, request
from util import importar_xls
from dotenv import load_dotenv

from Configuration.DbConection.queries import current_stock_query
from Configuration.DbConection.DbConnect import DbConnection

from json import dump, load
from pathlib import Path
from os import environ


load_dotenv()
app = Flask(__name__)
json_temp_path = Path(app.static_folder + '\\temp_json.json')
xls_temp_path = Path(app.static_folder + '\\abc.xls')

@app.get('/')
def index():
    return render_template("index.html")

@app.post('/xls')
def get_xls():
    
    if 'xlsFile' not in request.files:
        return "Nenhum arquivo enviado."
   
    json_path = json_temp_path
    xls_path = xls_temp_path
    xls = request.files['xlsFile']
    xls.save(xls_path)
    data = importar_xls(xls_path)

    if data:
        with open(json_path, 'w') as temp_json:
            dump(data, temp_json, indent=4)
        return redirect('/relatorio')


@app.get('/relatorio')
def relatorio():

    json_path = json_temp_path
    db_conn = DbConnection(
        
        environ['HOST'], 
        environ['PORT'], 
        environ['DBNAME'], 
        environ['USER'], 
        environ['PASSWD']
    )

    if not db_conn.connect():
        raise db_conn.error

    with open(json_path, 'r') as json_file:
        datas = load(json_file)
    
    if not isinstance(datas, list):
        raise ValueError('data should be a list') 
    
    
    response = db_conn.sqlquery(current_stock_query)

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
    
    
if __name__ == '__main__':
    app.run()
