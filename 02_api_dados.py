
import json, requests

Nome = input('Escreva o nome a ser localizado: ')
resposta = requests.get(f'https://servicodados.ibge.gov.br/api/v2/censos/nomes/{Nome}')

jsonDados = json.loads(resposta.text)
print(jsonDados[0]['res'][1])

