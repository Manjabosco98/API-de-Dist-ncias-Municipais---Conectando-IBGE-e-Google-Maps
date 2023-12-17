import requests
import googlemaps
import pandas as pd

# Chave da API do Google Maps
google_maps_api_key = 'chave_key'

# Função para obter todos os municípios do Brasil usando a API do IBGE
def obter_municipios():
    url_ibge = 'https://servicodados.ibge.gov.br/api/v1/localidades/municipios'
    response = requests.get(url_ibge)
    municipios = response.json()
    return municipios

# Função para calcular a distância entre duas cidades usando a API do Google Maps
def calcular_distancia(origem, destino, api_key):
    gmaps = googlemaps.Client(key=api_key)
    
    try:
        directions_result = gmaps.directions(origem, destino, mode="driving")
        
        if directions_result:
            if 'legs' in directions_result[0] and 'distance' in directions_result[0]['legs'][0]:
                distancia_km = directions_result[0]['legs'][0]['distance']['text']
                return distancia_km
            else:
                return "Sem informações de distância na resposta da API."
        else:
            return "Sem resultados da API para a rota desejada."
    except Exception as e:
        return f"Erro ao calcular distância: {str(e)}"

# Função para salvar os resultados em um DataFrame e exportar para Excel
def salvar_resultados_em_excel(resultados, nome_arquivo='distancias_entre_municipios.xlsx'):
    df_resultados = pd.DataFrame(resultados)
    df_resultados.to_excel(nome_arquivo, index=False)
    print(f'Resultados salvos em {nome_arquivo}')

# Função principal
def main():
    # Aparecida de Goiânia, GO - Pode alterar para a cidade desejada
    origem = 'Aparecida de Goiânia, GO'

    # Obter municípios do Brasil
    municipios = obter_municipios()

    # Lista para armazenar os resultados
    resultados = []

    # Calcular distância para cada município
    for municipio in municipios:
        destino = f"{municipio['nome']}, {municipio['microrregiao']['mesorregiao']['UF']['sigla']}"
        distancia = calcular_distancia(origem, destino, google_maps_api_key)
        resultados.append({'Origem': origem, 'Destino': destino, 'Distância': distancia})
        print(f'Distância de {origem} para {destino}: {distancia}')

    # Salvar os resultados em um DataFrame e exportar para Excel
    salvar_resultados_em_excel(resultados)

if __name__ == "__main__":
    main()
