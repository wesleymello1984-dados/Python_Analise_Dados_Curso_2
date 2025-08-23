import pandas as pd

# carregar dados da planilha

caminho = r'C:\Users\sabado\Desktop\Python AD - Wesley\01_base_vendas.xlsx'

df1 = pd.read_excel(caminho, sheet_name='Relatório de Vendas')
df2 = pd.read_excel(caminho, sheet_name='Relatório de Vendas1')

# exibiar as primeiras linhas da tabela

print('---------- Primeiro Relatório -----------')
print(df1.head())


print('---------- Segundo Relatório -----------')
print(df2.head())

# verificar se ha duplicatas
print('Duplicadtas no Relatório 01')
print(df1.duplicated().sum())

print('Duplicadtas no Relatório 02')
print(df2.duplicated().sum())

# consolidas as 2 tabelas

print('---- Dados Consolidados ----')
dfConsolidado = pd.concat([df1,df2],ignore_index=True)
print(dfConsolidado.head())

# exibir o número de clientes por cidade

clientePorcidade = dfConsolidado.groupby('Cidade')['Cliente'].nunique().sort_values(ascending=False)
print(clientePorcidade)

# número de vendas por plano

vendasPorplano = dfConsolidado['Plano Vendido'].value_counts()
print(vendasPorplano)

# exibir as 3 cidade com mais cliente

top3Cidades = clientePorcidade.head(3)
# top3Cidades = clientePorcidade.sort_values(ascending=False).head(3)
# cado não tivesse colocado o sort_values() na parte de cima do script

print ('---- Top 3 Cliente ----')
print(top3Cidades)

# adicionar uma nova coluna de status (exemplo fictício de analise)
# Classificar um plano como 'premium' se for enterprise, os demais serão 'padrão' 

dfConsolidado['status'] = dfConsolidado['Plano Vendido'].apply(lambda x: 'Premium' if x == 'Enterprise' else 'Padrão')
print(dfConsolidado)

# exibir a distribuição dos status

status = dfConsolidado['status'].value_counts()
print('---- Distribuição dos Status ----')
print(status)

# salvar a tabela em uma arquivo novo
# primeiro em Excel

dfConsolidado.to_excel('Dados_consolidados.xlsx', index=False)
print('Dados salvos na planilha do Excel')

# Depois em CSV
dfConsolidado.to_csv('Dados_consolidados.csv', index=False)
print('Dados salvos em CSV')

# Mensagem para finalizar

print('------ PROGRAMA FINALIZADO -----')