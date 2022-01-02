import requests
import pandas as pd
import json
import datetime

"""
Este código funciona 
Terminado em: 31/12/2021 às 01:18
update em: 31/12/2021 às 18:45 

Melhorias a se fazer
    - Pegar o número de páginas totais da categoria | ok
    - Gerar o json com a data especifica em uma pasta especifica | ok
    - Diminuir as linhas de código | ok
    - Inserir os outros valores no DataFrame (nome(ok), preço, multiplicador, marca(ok), tipo(ok), unit(ok), 
        photo_url(ok), url(ok)
        
    Acessar o price e pegar o price e o multiplier, dps inserir no dataframe 
"""

data = datetime.date.today()
data = str(data)

# Esvazia o arquivo para receber novos dados, por isso separar em uma pasta por data
# Além de tornar possivel fazer comparações de alteração de preço
with open('json-files/dados_atacadao-' + data + '.json', 'w') as arq:
    arq.truncate()


def busca_atacadao(tipo, pag):
    try:
        # url de acesso para pegar os dados, contatenando a categoria e a página
        url = 'https://www.atacadao.com.br/catalogo/search/?q=&category_id=' \
              'null&category[]={}&page={}&order_by=-relevance'.format(tipo, pag)
        r = requests.get(url)
        aux = r.text
        aux_dict = json.loads(aux)
        pag_exist = aux_dict['results']

        # Escreve no arquivo json os dados recebidos de cada página, de modo que os dados já escritos não sejam
        # sobrepostos, verifica se existe valor na key results, caso não exista, retorna uma variavel para parar o for
        if pag_exist:
            with open('json-files/dados_atacadao-' + data + '.json', 'a+') as arq:
                if pag != 2:
                    arq.write(',\n')
                arq.write(f'"pagina{pag}": ')
                arq.write(str(r.text))
        else:
            break_for = True
            return break_for

    finally:
        print(f'Página: {pag} foi lida')


def cria_json():
    with open('json-files/dados_atacadao-' + data + '.json', 'a+') as arq:
        arq.write('{')
        # For que inicia a função busca_atacadao e pega os dados do site, inserindo no json

    for i in range(2, 500):
        break_laco = busca_atacadao('oriental', i)
        if break_laco:
            break

    with open('json-files/dados_atacadao-' + data + '.json', 'a+') as arq:
        arq.write("}")  # Fecha o json


def exporta_excel():
    # O primeiro for busca os dados que estão dentro de duas listas e o segundo insere os dados corretamente em uma
    # unica lista que pode ser usada para gerar o DataFrame
    # Ainda não sei pq mas o pandas tem uma dificuldade pra trabalhar com dict, por isso é melhor usar list
    results = []
    with open('json-files/dados_atacadao-' + data + '.json') as file_json:
        read_content = json.load(file_json)
        for key, value in read_content.items():
            for key, val in value.items():
                if key == "results":
                    results.append(val)

    values = []
    for indice in results:
        for value in indice:
            values.append(value)

    price = []
    for indice in values:
        for key, value in indice.items():
            if key == 'price':
                price.append(value)

    price_prod = []
    multiplier = []
    for indice in price:
        for key, value in indice.items():
            if key == 'price':
                price_prod.append(value)
            elif key == 'multiplier':
                multiplier.append(value)

    print(multiplier)
    print(price_prod)
    df = pd.DataFrame(values).filter(items=['name', 'brand', 'type', 'unit', 'photo_url', 'url'])
    df.rename(columns={'name': 'Nome', 'brand': 'Marca', 'type': 'Tipo', 'unit': 'Unidade'}, inplace=True)
    df.insert(2, 'Preço', price_prod, allow_duplicates=False)
    df.insert(4, 'Multiplicador', multiplier, allow_duplicates=False)
    df.to_excel(r'C:\Users\gabri\PycharmProjects\Relatorio-Atacadao\AtacadRelat.xlsx')


cria_json()
exporta_excel()