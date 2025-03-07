import json
import jwt
from django.http import JsonResponse
from django.http import HttpResponse
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from .models import Licenca, Cliente, Endereco
from .aux_funcs_asaas import get_client
from .aux_func_woocommerce import get_order_by_id, obter_tipo_licenca


def home(request):
    return HttpResponse("Bem-vindo à página inicial!")

@csrf_exempt  # Isso desabilita a verificação CSRF, necessário para testar com um app de cliente externo
def validar_licenca(request):
    if request.method == "POST":
        
        auth_header = request.headers.get('Authorization', None)

        if not auth_header:
            return JsonResponse({"erro": "Cabeçalho Authorization não fornecido"}, status=400)
        
        # Verifica se o formato é 'Bearer <token>'
        if not auth_header.startswith('Bearer '):
            return JsonResponse({"erro": "Formato de token inválido. Use 'Bearer <token>'"}, status=400)
        
        token = auth_header[len('Bearer '):]  # Extrai o token sem a palavra 'Bearer '

        try:
            payload = Licenca.verificar_jwt(token)
            return JsonResponse({"status": "Licença válida", "dados": payload})
        except jwt.ExpiredSignatureError:
            return JsonResponse({"erro": "Token expirado"}, status=400)
        except jwt.InvalidTokenError as e:
            return JsonResponse({"erro": str(e)}, status=400)
    return JsonResponse({"erro": "Método inválido"}, status=405)

@csrf_exempt
def criar_cliente(request):
    if request.method == "POST":
        try:
            dados = json.loads(request.body)

            cliente = Cliente(
                wordpress_id=dados.get('wordpress_id'),
                nome=dados.get('nome'),
                email=dados.get('email'),
                )
            
            cliente.save()
            
            # Retornar sucesso com dados do cliente
            return JsonResponse({
                'message': 'Cliente criado com sucesso!',
                'cliente_id': cliente.id
            }, status=201)

        except Exception as e:
            print(f"Ocorreu o erro: {e}")
            # Retornar erro se algo falhar
            return JsonResponse({'error': f'Ocorreu um erro: {str(e)}'}, status=400)

@csrf_exempt
def processar_webhook(request):
    if request.method == "POST":
        try:
            # O webhook do Asaas deve nos enviar os dados do pagamento
            dados = json.loads(request.body)

            # Verifique o tipo de evento enviado
            tipo_evento = dados.get('event')
            if tipo_evento == 'PAYMENT_CONFIRMED':
                pagamento = dados.get('payment')
                id_cliente = pagamento.get('customer')
                id_order = pagamento.get('externalReference')
                dados_cliente = get_client(id_cliente)
                dados_venda = get_order_by_id(id_order)
                # Verficando se a licença é Mensal, Semestral ou Anual
                tipo_licenca = obter_tipo_licenca(dados_venda)

                try:
                    with transaction.atomic():
                        # Obtenha ou crie o cliente
                        cliente, created = Cliente.objects.get_or_create(
                            cpf_cnpj=dados_cliente.get('cpfCnpj'),
                            defaults={  # Campos que serão preenchidos se não existir
                                'asaas_id': dados_cliente.get('id'),
                                'tipo_pessoa': dados_cliente.get('personType'),
                                'nome': dados_cliente.get('name'),
                                'razao_social': dados_cliente.get('company'),
                                'inscricao_municipal': dados_cliente.get('municipalInscription'),
                                'inscricao_estadual': dados_cliente.get('stateInscription'),
                                'email': dados_cliente.get('email'),
                                'telefone_1': dados_cliente.get('phone'),
                                'telefone_2': dados_cliente.get('mobilePhone'),
                            }
                        )
                        
                        if created:
                            print("Cliente criado com sucesso...\n")
                        else:
                            print("Cliente já existente.")
                        
                        # Verifica se o endereço já existe para este cliente
                        endereco_existente = Endereco.objects.filter(
                            cliente=cliente,
                            logradouro=dados_cliente.get('address'),
                            numero=dados_cliente.get('addressNumber'),
                            complemento=dados_cliente.get('complement'),
                            bairro=dados_cliente.get('province'),
                            cep=dados_cliente.get('postalCode'),
                            cidade=dados_cliente.get('cityName'),
                            estado=dados_cliente.get('state'),
                            pais=dados_cliente.get('country'),
                        ).exists()

                        if not endereco_existente:
                            Endereco.objects.create(
                                cliente = cliente,
                                logradouro = dados_cliente.get('address'),
                                numero = dados_cliente.get('addressNumber'),
                                complemento = dados_cliente.get('complement'),
                                bairro = dados_cliente.get('province'),
                                cep = dados_cliente.get('postalCode'),
                                cidade = dados_cliente.get('cityName'),
                                estado = dados_cliente.get('state'),
                                pais = dados_cliente.get('country'),
                                )
                            
                            print("Endereço criado com sucesso...\n")
                        else:
                            print("Endereço já existe para este cliente.")

                        Licenca.objects.create(
                            cliente = cliente,
                            status = 'ativa',
                            tipo_licenca = tipo_licenca.lower(),
                        )

                        print("Licença criada com sucesso.\n")

                except Exception as e:
                    print(f"Ocorreu um erro: {e}")
                    return JsonResponse({"error": f"Erro ao processar dados: {str(e)}"}, status=400)
                
                return JsonResponse({"message": "Licença processada com sucesso"}, status=200)
            
            elif tipo_evento == 'PAYMENT_CREATED':
                print(f"TESTE PARA {tipo_evento}")
                return JsonResponse({"message": f"TESTE PARA {type} bem sucedido"}, status=200)
            
        except json.JSONDecodeError:
            print("Erro ao decodificar JSON.")
            return JsonResponse({"error": "Erro no formato do JSON recebido."}, status=400)

        except Exception as e:
            print(f"Erro inesperado: {e}")
            return JsonResponse({"error": "Erro interno no servidor."}, status=500)
    
    else:
        return JsonResponse({"message": "Requisição inválida."}, status=400)
                    
@csrf_exempt
def teste_webhook(request):
    if request.method == "POST":
        try:
            # O webhook do Asaas deve nos enviar os dados do pagamento
            dados = json.loads(request.body)
            

            # Verifique o tipo de evento enviado
            tipo_evento = dados.get('event')
            if tipo_evento == 'PAYMENT_CONFIRMED':
                pagamento = dados.get('payment')
                id_cliente = pagamento.get('customer')
                id_order = pagamento.get('externalReference')
                dados_cliente = get_client(id_cliente)
                dados_venda = get_order_by_id(id_order)
                
                print("DADOS DA VENDA/PRODUTO")
                print(json.dumps(dados_venda, indent=4))
                
                # print(tipo_evento)
                # print(json.dumps(dados, indent=4))
                return JsonResponse({"message": f"TESTE: {tipo_evento}, bem sucedido"}, status=200)
            
            elif tipo_evento == 'PAYMENT_CREATED':
                print(tipo_evento)
                print(json.dumps(dados, indent=4))
                return JsonResponse({"message": f"TESTE: {tipo_evento}, bem sucedido"}, status=200)
            
        except json.JSONDecodeError:
            print("Erro ao decodificar JSON.")
            return JsonResponse({"error": "Erro no formato do JSON recebido."}, status=400)

        except Exception as e:
            print(f"Erro inesperado: {e}")
            return JsonResponse({"error": "Erro interno no servidor."}, status=500)
    
    else:
        return JsonResponse({"message": "Requisição inválida."}, status=400)