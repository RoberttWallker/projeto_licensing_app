import random
import string


def gerar_sku(prefixo="ND", tamanho_sequencia=8):
    # Gerar parte aleatória com letras e números
    aleatorio = ''.join(random.choices(string.ascii_uppercase + string.digits, k=tamanho_sequencia))
    
    # Criar o SKU no formato desejado
    sku = f"{prefixo}-{aleatorio}"
    
    return sku