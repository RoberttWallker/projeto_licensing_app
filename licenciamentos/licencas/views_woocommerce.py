from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .aux_func_woocommerce import get_order_by_id, auth_signature_wc_webhook
import json
import traceback
from json import JSONDecodeError
from django.conf import settings


@csrf_exempt
def get_order_wc(request, id):
    if request.method == "GET":
        response = get_order_by_id(id)
        if response.status_code == 200:
            return JsonResponse(response.json(), safe=False)
        else:
            return JsonResponse({"erro": "Erro ao obter pedido do Woocommerce"}, status=response.status_code)
    
    return JsonResponse({"erro": "Método não permitido"}, status=405)


@csrf_exempt
def webhook_orders_wc(request):
    if request.method == "POST":
        try:
            if not request.body.strip():
                print('Corpo de requisição vazio.')
                return JsonResponse({"error": "Corpo da requisição está vazio"}, status=400)

            # Obtém o cabeçalho e o corpo da requisição
            headers = request.headers
            signature = headers.get("X-Wc-Webhook-Signature")
            secrets = settings.WEBHOOK_ORDERS_SECRETS

            if not signature:
                print("\nNenhuma assinatura foi recebida!")
                return JsonResponse({"erro": "Nenhuma assinatura foi recebida."}, status=400)

            # Verifica a assinatura
            authorization = auth_signature_wc_webhook(request.body, signature, secrets)

            if authorization:                
                try:
                    dados = json.loads(request.body.decode("utf-8"))
                except JSONDecodeError as e:
                    return JsonResponse({"error": f"Erro ao processar JSON: {str(e)}"}, status=400)
                
                # Dados da requisição
                id = dados.get("id")
                status = dados.get("status")
                customer_id = dados.get("customer_id")
                total_value = dados.get("total")

                tipo_evento = headers.get('X-Wc-Webhook-Topic')

                if tipo_evento == "order.created":
                    print("TESTE ORDEM/PEDIDO CRIADA")
                    print(f"ID VENDA: {id}, STATUS: {status}, ID CLIENTE: {customer_id}, VALOR: {total_value}")

                elif tipo_evento == "order.updated":
                    print("TESTE ORDEM/PEDIDO ATUALIZADA")
                    print(f"ID VENDA: {id}, STATUS: {status}, ID CLIENTE: {customer_id}, VALOR: {total_value}")

                elif tipo_evento == "order.deleted":
                    print("TESTE ORDEM/PEDIDO DELETADA")
                    print(f"ID VENDA: {id}, STATUS: {status}, ID CLIENTE: {customer_id}, VALOR: {total_value}")
                
                else:
                    print("Tipo de evento não rastreado.")
        
                return JsonResponse({"message": "Teste processado com sucesso"}, status=200)
            
            else:
                return JsonResponse({"error": "Assinatura inválida"}, status=400)
        
        except Exception as e:
            traceback.print_exc()
            return JsonResponse({"error": f"Erro ao processar dados: {str(e)}"}, status=400)
                
