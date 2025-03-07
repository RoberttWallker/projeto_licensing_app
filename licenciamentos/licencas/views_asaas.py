from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .aux_funcs_asaas import list_clients, get_client

@csrf_exempt
def list_clients_view(request):
    """View para listar os clientes"""
    if request.method == "GET":
        response = list_clients()  # Chama a função list_clients
        
        if response.status_code == 200:
            return JsonResponse(response.json(), safe=False)
        else:
            return JsonResponse({"erro": "Erro ao obter clientes do Asaas"}, status=response.status_code)
    
    return JsonResponse({"erro": "Método não permitido"}, status=405)


@csrf_exempt
def get_client_view(request, client_id):
    """View para obter um cliente específico por ID"""
    if request.method == "GET":
        response = get_client(client_id)  # Chama a função get_client
        
        if response.status_code == 200:
            return JsonResponse(response.json(), safe=False)
        else:
            return JsonResponse({"erro": "Erro ao obter cliente do Asaas"}, status=response.status_code)
    
    return JsonResponse({"erro": "Método não permitido"}, status=405)