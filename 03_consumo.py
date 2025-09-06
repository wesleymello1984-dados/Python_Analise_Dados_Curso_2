from flask import Flask, request, render_template_string
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.io as pio
import random as rd
import os

pio.renderers.default = 'browser'

#carregar o arquivo drinks

# ________opção 1____________

# dfDrinks = pd.read_csv(r"C:\Users\sabado\Desktop\Python AD - Wesley\drinks.csv")

# caminho = "C:/Users/sabado/Desktop/Python AD - Wesley/"
# tabela1 = "drinks.csv"
# tabela2 = "avengers.csv"

# dfDrinks = pd.read_csv(f'{caminho},{tabela1}')
# dfAvengers = pd.read_csv(f'{caminho},{tabela2}')

# ________opçao 2____________
caminho = "C:/Users/sabado/Desktop/Python AD - Wesley/"
tabela = ["drinks.csv","avengers.csv"]
codHtml = '''
    <h1> Dashboards - Consumo de Alcool </h1>
    <h2> Parte 01 </h2>
        <ul>
            <li><a href='/grafico1'> Top 10 paises em consumo de alcool </a></li>
            <li><a href='/grafico2'> Média de consumo por Tipo </a></li>
            <li><a href='/grafico3'> Consumo total por Região </a></li>
            <li><a href='/grafico4'> Comparativo entre tipo de bebidas </a></li>
            <li><a href='/pais'> Insights por pais </a></li>
        </ul>
    <h2> Parte 02 </h2>
        <ul>
            <li><a href='/comparar'> Comparar </a></li>
            <li><a href='/upload'> Upload CSV Vingadores </a></li>
            <li><a href='/apagar'> Apagar Tabela </a></li>
            <li><a href='/ver'> ver Tabela </a></li>
            <li><a href='/vaa'> V.A.A (Vingadores Alcoolicos Anônimos </a></li>
        </ul>
        
'''

def carregarCsv():

    try:
        dfDrinks = pd.read_csv(os.path.join(caminho,tabela[0]))
        dfAvengers = pd.read_csv(os.path.join(caminho,tabela[1]),encoding='latin1')
        return dfDrinks, dfAvengers

    except Exception as erro:
        print(f'Erro ao carregar os arquivos csv: {erro}')
        return None, None

def criarBancoDados ():
    conn = sqlite3.connect(f'{caminho}banco 01.bd')
# carregar dados usando nossa função criada anteriormente
    dfDrinks, dfAvengers = carregarCsv()
    if dfDrinks is None or dfAvengers is None:
        print('Falha ao carregar os dados!!!')
        return
    
# inserir as tabelas noa banco de dados
    dfDrinks.to_sql('bebidas',conn, if_exists='replace', index=False)
    dfAvengers.to_sql('vingadores', conn, if_exists='replace', index=False)
    conn.commit()
    conn.close()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string (codHtml)

@app.route('/grafico1')
def grafico1():
    with sqlite3.connect(f'{caminho}banco 01.bd') as conn:
        df = pd.read_sql_query('''
            SELECT country, total_litres_of_pure_alcohol
            FROM bebidas
            ORDER BY total_litres_of_pure_alcohol DESC
            LIMIT 10
''', conn)
                
    figuraGrafico01 = px.bar(
        df,
        x = 'country',
        y = 'total_litres_of_pure_alcohol',
        title = 'Top 10 paises com maior consumo de alcool'
    )
        
    return figuraGrafico01.to_html()

@app.route ('/grafico2')
def grafico2():
    with sqlite3.connect(f'{caminho}banco 01.bd') as conn:
        df = pd.read_sql_query('''
            SELECT AVG(beer_servings) AS cerveja, 
            AVG(spirit_servings) AS destilados, 
            AVG(wine_servings) AS vinhos FROM bebidas
        ''', conn)
        
    df_melted = df.melt(var_name='Bebidas',value_name='Média de Porções')
    figuraGrafico02 = px.bar(
        df_melted,
        x = 'Bebidas',
        y = 'Média de Porções',
        title = 'Média de consumo global por tipo'
    )
    return figuraGrafico02.to_html()

@app.route('/grafico3')
def grafico3():
    regioes = {
        'Europa':['France','Germany','Spain','Italy','Portugal'],
        'Asia':['China','Japan','India','Thailand'],
        'Africa':['Angola','Nigeria','Egypt','Algeria'],
        'Americas':['USA','Canada','Brazil','Argentina','Mexico']
    }
    dados = []
    with sqlite3.connect(f'{caminho} banco 01.bd') as conn:
        # itera sobre o dicionario, de regioes onde cada chave (regiao tem uma lista de pises)
        for regiao, paises in regioes.items():
            placeholders = ",".join([f"'{pais}'" for pais in paises])
            query = f'''
                SELECT SUM(total_litres_of_pure_alcohol) AS Total
                FROM bebidas
                WHERE country IN ({placeholders})
            '''
            total = pd.read_sql_query(query, conn).iloc[0,0]
            dados.append({
                    "Região": regioes,
                    "Consumo Total": total
            })

        df_regioes = pd.DataFrame(dados)
        figuraGrafico03 = px.pie(
            df_regioes,
            names = 'Região',
            values = 'Consumo Total',
            title = 'Consumo total por Região'
        )
    return figuraGrafico03.to_html()

@app.route('/comparar', methods=['POST','GET'])
def comparar():
    opcoes = [
        'beer_servings',
        'spirit_servings',
        'wine_servings'
    ]

    if request.method == "POST":
        eixoX = request.form.get('eixo_x')
        eixoY = request.form.get('eixo_y')
        if eixoX == eixoY:
            return "<marquee> Você fez besteira ... escolha tabelas diferentes </marquee>"
        conn = sqlite3.connect(f'{caminho}banco01.bd')
        df = pd.read_sql_query("SELECT country, {}, {} FROM bebidas".format(eixoX, eixoY),conn)
        conn.close()

        figuraComparar = px.scatter(
            df,
            x = eixoX,
            y = eixoY,
            title = f'Comparação entre {eixoX} VS {eixoY}'
        )
        figuraComparar.update_traces(textposition = "top center")

        return figuraComparar.to_html()
    
    
    return render_template_string('''
            <!-- Isso é um comentátio dentro do HTML -->
            <style>
                /* Estilo global com tema escuro neutro */
    body {
        background-color: #1e1e1e;
        color: #e0e0e0;
        font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
        margin: 40px;
        line-height: 1.6;
    }

    /* Título principal */
    h2 {
        font-size: 28px;
        color: #f0f0f0;
        border-bottom: 2px solid #333;
        padding-bottom: 10px;
        margin-bottom: 30px;
    }

    /* Todos os <form> no site */
    form {
        background-color: #2c2c2c;
        padding: 30px;
        border-radius: 10px;
        box-shadow: 0 0 15px rgba(0, 0, 0, 0.4);
        max-width: 400px;
    }

    /* Rótulos dos campos */
    label {
        display: block;
        margin-bottom: 6px;
        font-weight: bold;
        color: #cccccc;
        font-size: 15px;
    }

    /* Estilo dos <select> */
    select {
        width: 100%;
        padding: 10px;
        background-color: #3a3a3a;
        color: #e0e0e0;
        border: 1px solid #555;
        border-radius: 6px;
        margin-bottom: 20px;
        font-size: 14px;
        appearance: none;
        outline: none;
        transition: border 0.3s ease;
    }

    select:hover, select:focus {
        border-color: #888;
    }

    /* Botão de envio */
    input[type="submit"] {
        background-color: #444;
        color: #fff;
        padding: 12px 20px;
        border: none;
        border-radius: 6px;
        font-size: 14px;
        cursor: pointer;
        transition: background-color 0.3s ease, transform 0.2s ease;
        width: 100%;
    }

    input[type="submit"]:hover {
        background-color: #555;
        transform: scale(1.02);
    }

    input[type="submit"]:active {
        background-color: #333;
        transform: scale(0.98);
    }

    /* Estilizar quebras de linha apenas para espaçamento */
    br {
        display: block;
        margin: 10px 0;
    }
    </style>

            <h2> Comparar Campos </h2>
            <form method="POST">
                <label for="eixo_x"> Eixo X: </label>
                <select name="eixo_x">
                                    
                {% for opcao in opcoes %}                   
                    <option value="{{opcao}}"> {{opcao}} </option>
                {% endfor %} 
                                                        
                </select>
                <br></br>
                                    
                <label for="eixo_y"> Eixo Y: </label>
                <select name="eixo_y">
                    {% for opcao in opcoes %}
                    <option value="{{opcao}}" > {{opcao}} </option>
                    {% endfor %}

                </select>
                <br></br>
                                    
                <input type="submit" value="-- Comparar ---">
            </form>
    ''', opcoes = opcoes)

@app.route('/ver', methods=['POST','GET'])
def ver_tabela():
    if request.method == 'POST':
        nome_tabela = request.form.get('tabela')
        if nome_tabela not is ['bebidas','veingadores']:
            return "Tabela errada rapaz...pensa que vai onde?"
        conn = sqlite3,connect(f'{caminho}banco01.bd')
        df = pd.read_sql_query(f'SELECT * FROM {nome_tabela}', conn)
        conn.close()
        tabela_html = df.to_html(clases='table table-striped')
        return f'''
        <h3> Conteudo do tabela {nome_tabela} : </h3>
        {tabela_html}
        '''
    return render_template_string('''
            <h3> Visualizar Tabelas </h3>
            <form>
            <label for='Tabela'> Selecione uma tabela> </label>
            <select name='Tabela'>
                <option name='bebidas'> Bebidas </option>
                <option name='vingadores'> Vingadores </option>
            </select>
            <input type='submit' value='Consultar'>

''')


@app.route('/upload', method=['GET','POST'])
def upload ():
    if request.method == 'POST':
        recebido = request.files['c_arquivo']
        if not recebido:
            return "Nenhum arquivo foi recebido"
        dfAvengers = pd.read_csv(recebido, encoding='latin1')
        conn = sqlite3,connect(f'{caminho}banco01.bd')
        dfAvengers.to_sql("Vingadores", conn, if_exists="replace", index=False)
        conn.commit()
        conn.close()
        return "Sucesso! Tabela vingadores armazenada no banco de dados"

    return '''
        <h2> Upload da tabela Avengers </h2>
        <form method='POST' enctype='multipart/form-data'>
            <input type='file' name='c_arquivo' accept=',csv'>
            <input type='submit' value='Carregar'>
        </form>
    '''


if __name__ == '__main__':
    criarBancoDados ()
    app.run(debug=True)


