"""
URL configuration for licenciamentos project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from licencas.views import validar_licenca, home, criar_cliente, processar_webhook, teste_webhook
from licencas.views_asaas import list_clients_view, get_client_view
from licencas.views_woocommerce import get_order_wc, webhook_orders_wc


urlpatterns = [
    #---------------------------------------------------------------------------#
    # PATHS PADRÃO
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    #---------------------------------------------------------------------------#
    # PATHS INTERNAS
    path('api/criar_cliente/', criar_cliente),
    path('api/validar_licenca/', validar_licenca),
    #---------------------------------------------------------------------------#
    # PATHS ASAAS WEBHOOK EVENTOS
    path('asaas/webhook/', processar_webhook),
    # PATHS ASAAS ACESSAR FUNCIONALIDADES DA API ASAAS
    path('asaas/clientes/', list_clients_view, name='clientes'),
    path('asaas/clientes/<str:client_id>/', get_client_view, name='cliente'),
    #---------------------------------------------------------------------------#
    # PATHS WOOCOMMERCE WEBHOOK EVENTOS
    path('woocommerce/webhook/orders/', webhook_orders_wc),
    # PATHS WOOCOMMERCE ACESSAR FUNCIONALIDADE DA API WOOCOMMERCE
    path('api/woocommerce/<str:id>/', get_order_wc),
    #---------------------------------------------------------------------------#
    # PATHS DE TESTES
    path('api/webhook/teste_webhook/', teste_webhook),
]
