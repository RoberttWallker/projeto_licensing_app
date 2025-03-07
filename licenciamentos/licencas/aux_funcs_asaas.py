import requests
from django.conf import settings

URL_ASAAS_CLIENTES = settings.URL_ASAAS_CLIENTES
ASAAS_API_KEY = settings.ASAAS_API_KEY


def list_clients():
    headers = {
        "accept": "application/json",
        "access_token": ASAAS_API_KEY
        }

    response = requests.get(URL_ASAAS_CLIENTES, headers=headers)

    return response.json()

def get_client(id):
    url = f"{URL_ASAAS_CLIENTES}/{id}"

    headers = {
        "accept": "application/json",
        "access_token": ASAAS_API_KEY
        }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        # Retorna o corpo da resposta como um dicionário JSON
        return response.json()
    else:
        # Lidar com erros (como status 404 ou 500)
        raise Exception(f"Erro ao obter dados do cliente {id}: {response.text}")
