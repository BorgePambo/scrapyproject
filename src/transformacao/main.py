##vamos importar o arquivo que precisamos
import pandas as pd
import sqlite3
from datetime import datetime

###setar para mostrar todas as colunas do pandas
pd.options.display.max_columns = None

##Definir o arquivo json 
dframe = pd.read_json('../data/data.json')


##pd.options.display.max_coluns = None

#Adicionar a coluna _source com um valor fixo
dframe['_source'] = 'https://lista.mercadolivre.com.br/tenis-corrida-masculino'

#Adicionar a coluna da _data_coleta com a data e hora atual
dframe['_data_coleta'] = datetime.now()

# for coluna in dframe.columns:
#     print(coluna)

## print(dframe.info())

## Tratar os valores nulos para colunas númerica e do texto
dframe['old_price_centavos'] = dframe['old_price_centavos'].fillna(0).astype(float)
dframe['new_price_centavos'] = dframe['new_price_centavos'].fillna(0).astype(float)
dframe['old_price_reais'] = dframe['old_price_reais'].fillna(0).astype(float)
dframe['new_price_reais'] = dframe['new_price_reais'].fillna(0).astype(float)
dframe['rating'] = dframe['rating'].fillna(0).astype(float)


# Remove os parênteses das strings na coluna 'reviews'
dframe['reviews'] = dframe['reviews'].str.replace(r'[\(\)]', '', regex=True)

# Preenche valores vazios com 0 e converte a coluna para o tipo int
dframe['reviews'] = dframe['reviews'].fillna(0).astype(int)

#Tratar os precos como floats e calcular os valores totais
dframe['old_price'] = dframe['old_price_reais'] + dframe['old_price_centavos'] / 100
dframe['new_price'] = dframe['new_price_reais'] + dframe['new_price_centavos'] / 100

# Remove as colunas do DataFrame original
dframe.drop(columns=['old_price_reais', 'new_price_reais', 'old_price_centavos', 'new_price_centavos'], inplace=True)


# Conectar ao banco de dados SQLite (Ou criar um novo)
conn = sqlite3.connect('../data/quotes.db')

# Salvar o banco de dados no banco de dados SQLite
dframe.to_sql('mercadolivre_items', conn, if_exists='replace', index=False)

# Fechar a conexao com o banco de dados
conn.close()

## Salvar o dataframe em csv
dframe.to_csv('../data/relatorio.csv', index=False)

