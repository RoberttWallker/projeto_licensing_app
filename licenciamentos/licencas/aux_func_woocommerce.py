import requests
import base64
from django.conf import settings
import hmac
import hashlib

WC_ORDERS_URL = settings.WC_ORDERS_URL
WC_CONSUMER_KEY = settings.WC_CONSUMER_KEY
WC_CONSUMER_SECRET = settings.WC_CONSUMER_SECRET

def get_order_by_id(id):
    # Url de ordens com id no final
    url_ordem = f"{WC_ORDERS_URL}/{id}"
    print(f"URL gerada: {url_ordem}")
    response = requests.get(url_ordem, auth=(WC_CONSUMER_KEY, WC_CONSUMER_SECRET))
    if response.status_code == 200:
        return response.json()
    else:
         # Lidar com erros (como status 404 ou 500)
        raise Exception(f"Erro ao obter dados do cliente {id}: {response.text}")
    
# Acessando os line_items e meta_data
def obter_tipo_licenca(dados_venda):
    # Verificar se 'line_items' está presente
    if 'line_items' in dados_venda:
        for item in dados_venda['line_items']:
            # Verificar se 'meta_data' está presente dentro do item
            if 'meta_data' in item:
                for meta in item['meta_data']:
                    # Acessar o 'value' do meta_data
                    if meta.get('key') == 'tipo' and 'value' in meta:  # Se for o valor desejado (por exemplo, "Mensal")
                        return meta['value']
    return None  # Caso não encontre


def auth_signature_wc_webhook(body, signature_received, secrets=None):
    if not secrets:
        print("\nNenhuma lista de Secrets foi passada!")
        return False
    
    # Decodifica a assinatura recebida (Base64 → bytes)
    try:
        signature_decoded = base64.b64decode(signature_received).hex()
    except Exception as e:
        print(f"\nErro ao decodificar a assinatura recebida: {e}")
        return False
    
    for secret in secrets:
        # Calcula a assinatura HMAC-SHA256
        signature_calculated = hmac.new(
            secret.encode('utf-8'),   # Chave secreta
            body,                     # Corpo da requisição
            hashlib.sha256            # Algoritmo SHA-256
        ).hexdigest()

        # Compara a assinatura recebida com a calculada
        if hmac.compare_digest(signature_decoded, signature_calculated):
            print("\nAssinatura válida")
            return True
        
    print("\nAssinatura inválida.")
    return False