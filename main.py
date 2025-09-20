#  ___       ___    _____    _____   _____        _____  __      __
# (  (       )  )  / ___/   / ____\ (_   _)      / ___/  ) \    / (
#  \  \  _  /  /  ( (__    ( (___     | |       ( (__     \ \  / / 
#   \  \/ \/  /    ) __)    \___ \    | |        ) __)     \ \/ /  
#    )   _   (    ( (           ) )   | |   __  ( (         \  /   
#    \  ( )  /     \ \___   ___/ /  __| |___) )  \ \___      )(    
#     \_/ \_/       \____\ /____/   \________/    \____\    /__\   
                                                                 
#    __    __      _____   _____       _____         ____          
#    \ \  / /     / ___/  (_   _)     (_   _)       / __ \         
#    () \/ ()    ( (__      | |         | |        / /  \ \        
#    / _  _ \     ) __)     | |         | |       ( ()  () )       
#   / / \/ \ \   ( (        | |   __    | |   __  ( ()  () )       
#  /_/      \_\   \ \___  __| |___) ) __| |___) )  \ \__/ /        
# (/          \)   \____\ \________/  \________/    \____/         

# autor: Wesley Mello
# Data: 20/09/2025
# versão: 1.0.0

from flask import Flask, request, jsonify, render_template_string
import pandas as pd
import sqlite3
import os
import plotly.graph_objs as go
from dash import Dash, html, dcc
import numpy as np
import config                               # Nosso config.py
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

app = Flask (__name__)
pasta = config.folder
caminhoBd = config.bd_path
rotas = config.rotas
vazio = 0

def init_db():
    with sqlite3.connect(f'{pasta}{caminhoBd}') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS inadimplencia (
                       mes TEXT PRIMARY KEY,
                       inadimplencia REAL)
''')
        
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS selic (
                       mes TEXT PRIMARY KEY,
                       selict_diaria REAL)
''')
        
        conn.commit()

@app.route(rotas[0])   
def index():
    return render_template_string (f'''
        <h1> Upload dados Economicos </h1>
        <form action="" mathod-"POST" enctype="multipart/form-data">
                                   
            <label for="campo_inadimplencia"> Arquivo de Inadimplencia (CSV): </label>
            <input name="campo_inedimplencia" type="file" required>

            <label for="campo_selic"> Arquivo de Taxa Selic (CSV): </label>
            <input name="campo_selic" type="file" required>

            <input type="submit" value="Fazer Upload">
        
        </form>
        <br><br>

        <a href="{rotas[2]}"> Consulyar dados Armazenados </a> <br>
        <a href="{rotas[3]}"> Visualizar Graicos </a> <br>
        <a href="{rotas[4]}"> Editar Inadimplencia </a> <br>
        <a href="{rotas[5]}"> Analisar Correlação </a> <br>
                                
''')

@app.route(rotas[1], methods=['POST','GET'])
def upload():
    inad_file = request.files.get('campo_inadimplencia')
    selic_file = request.files.get('campo_selic')

    if not inad_file or not selic_file:
        return jsonify({'Erro':'Ambos os arquivos devem ser enviados.'}), 406
    
    inad_df = pd.read_csv(
        inad_file,
        sep = ';',
        names = ['data','inadimplencia'],
        header = 0
    )

    selic_df = pd.read_csv(
        selic_file,
        sep = ';',
        names = ['data','selic_diaria'],
        header = 0  
    )
    inad_df['data']=pd.to_datetime(
        inad_df['data'],
        format='%d/%m/%y'
    )
    selic_df['data']=pd.to_datetime(
        inad_df['data'],
        format='%d/%m/%Y'
    )
    inad_df['mes'] = inad_df['data'].dt.to_period('M').astype(str).drop_duplicates()
    selic_df['mes'] = selic_df['data'].dt.to_period('M').astype(str)

    # inad_df['mes'] = inad_df[['mes','inadimplencia']].drop_duplicates()
    selic_mensal = selic_df.groupby('mes')['selic_diaria'].mean().reset_index()

    with sqlite3.connect(f'{pasta}{caminhoBd}') as conn:
        inad_df.to_sql(
            'inadimplencia',
            conn,
            if_exists= 'replace',
            index = False
        )
        selic_df.to_sql(
            'selic',
            conn,
            if_exists= 'replace',
            index = False
        )
    return jsonify ({'Mensagem': 'Dados cadastrados com sucesso!'}), 200

@app.route(rotas[2], methods=['POST','GET'])
def consultar():
    if request.method == "POST":
        tabela = request.form.get('campo_tabela')
        if tabela not in ['inadimplencia','selic']:
            return jsonify({'Erro':'Tabela é invalida'}), 400
        with sqlite3.connect(f'{pasta}{caminhoBd}') as conn:
            df = pd.read_sql_query(f'SELECT * FROM {tabela}', conn)
        return df.to_html(index=False)


    return render_template_string (f'''
        <h1> Consulta de tabelas </h1>
        <form method="POST">
            <label for='campo_tabela'> Escolha uma tabela: </label>
            <select name='campo_tabela'>
                <option value='inadimplencia'> Inadimplência </option>
                <option value='selic'> Taxa Selic </option>
                <option value='usuarios'> Usuários </option>
            </select>
            <imput type="submit" value="Consultar">
        </form>
        <br>
        <a href='{rotas[0]}'> Voltar </a>
''')

@app.route(rotas[4], methods=['POST','GET'])
def editar_inadimplencia():

    
    if request.method =="POST":
        mes = request.form.get('campo_mes')
        novo_valor = request.form.get('campo_valor')
        try:
            novo_valor = float(novo_valor)
        except:
            return jsonify({'Erro':'Valor Invalido'}),418
        with sqlite3.connect(f'{pasta}{caminhoBd}') as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE inadimplencia
                SET inadimplencia = ?
                WHERE mes = ?
    ''', (novo_valor, mes))
            conn.commit()
        return jsonify ({'Mensagem':f'Valor atualizado para o mes {mes}'})         



    return render_template_string (f'''
        <h1> Editar Inadimplência </h1>
            <form method="POST">
                <label for='campo_mes'> Mês (AAAA-MM): </label>
                <input type='text' name='campo_mes'><br> 
                                                                     
                <label for='campo_mes'> Novo valor: </label>
                <input type='text' name='campo_valor'><br>

                <input type='submit' value='Salvar'>
            </form>
            <br>
            <a href='{rotas[0]}'> Voltar </a>
''')

@app.route(rotas[5])
def correlacao():
    with sqlite3.connect(f'{pasta}{caminhoBd}') as conn:
        inad_df = pd.read_sql_query('SELECT * FROM inadimplencia', conn)
        selic_df = pd.read_sql_query('SETECT * FROM selic', conn)

    # realiza uma junção entre os dois detaframes usando a coluna de mes como chave
    merged = pd.merget(inad_df, selic_df, on='mes')

    # calcular o coeficiente da correlação de pearson entre as duas variáveis
    correl = merged['inadimplencia'].corr(merged['selic_diaria'])

    # registra as variáveis para a regressão linear  onde X é a variável independente e Y é a variável dependente
    X = merged['selic_diaria']
    Y = merged['inadimplencia']

    # calcula o coeficiente da reta de regrassão linerar onde M é a inclinadação e B é a interseção
    m, b = np.polyfit(X, Y, 1)

    # Oba!!! Gráficos ☺

    fig = go.Figure()
    fig.add_trace(go.Scetter(
        X = X,
        Y = Y,
        mode = 'markers',
        name = 'Inadimplencia x Selic',
        marker = dict(
            color = 'rgba(0, 123, 255, 0.8)',
            size = 12,
            line = dict(width = 2, color = 'white'),
            symbol = 'circle'
        ),
        hovertemplate = 'Selic: %{X:.2f}% <br> Inadimplencia: %{Y:.2f}% <extra></extra>'
    ))
    fig.add_trace(go.Scatter(
        X = X,
        Y = m * X + b,
        mode = 'lines',
        line = dict(
            color = 'rgba(255, 53, 69, 1)', 
            width = 4,
            dash = 'dot'
        )
    ))
    fig.update_layout(
        title = {
            'text': f'<b> Correlação entre Selic e Inadimplência </b><br><span style="font-size:16px;"> Coeficiência de Correlação: {correl:.2f} </span>',
            'Y':0.95,
            'X':0.5,
            'xanchor' : 'center',
            'yanchor' : 'top'
        },
        xaxis_title = dict(
            text = 'SELIC Média mensal (%)',
            font = dict(
                size = 18,
                family = 'Arial',
                color = 'gray'
                )
        ),
        yaxis_title = dict(
            text = 'inadimplência',
            font = dict(
                size = 18,
                family = 'Arial',
                color = 'gray'
                )
        ),
        xaxis = dict(
            tickfont = dict(
                size = 14,
                family = 'Arial',
                color = 'black'
                ),
                gridcolor = 'lightgray'
        ),
        yaxis = dict(
            tickfont = dict(
                size = 14,
                family = 'Arial',
                color = 'black'
                ),
                gridcolor = 'lightgray'
        ),
        font = dict(
            size = 14,
            family = 'Arial',
            color = 'black'
        ),
        legend = dict(
            orientation = 'h',
            yanchor = 'bottom', 
            xanchor = 'center',
            X = 0.5,
            Y = 1.05,
            bgcolor = 'rgba(0,0,0,0)',
            borderwidth = 0
        ),
        margin = dict(l = 60, r = 60, t = 120, b = 60),
        plot_bgcolor = '#f8f9fa',
        paper_bgcolor = 'white'
    )
    graph_html = fig.to_html(
        full_html = False,
        include_ploplyjs = 'cdn'
    )
    return render_template_string('''
    <html>
        <head>
                <title> Correlação Selic x Inadimplência </title>
        </head>
        <body>
            <h1> Correlação Selic x Inadimplência </h1>
            <div>{{ grafico|safe }}</div>
            <br>                                
            <a href="{{ Voltar }}"> Voltar </a>
        </body>
    </html>
''', grafico = graph_html, voltar = rotas[0])



if __name__ == '__main__':
    init_db()
    app.run(
        debug= config.flask_debug,
        host= config.flask_host,
        port= config.flask_port
    )




