# projeto_licensing_app

Este é um projeto Django para criação e gerenciamento de **licenças** com integração ao **Woocommerce** e ao **gateway de pagamentos Asaas**. O aplicativo tem como objetivo facilitar a gestão de licenças para um portfólio de produtos, com funcionalidades para criação de pedidos, cupons, clientes e integração com o sistema de pagamento Asaas.

## Tecnologias

- Django 5.1.6
- MySQL
- API Woocommerce
- API Asaas

## Funcionalidades

- Criação e gerenciamento de **licenças**.
- Integração com a **API do Woocommerce** para gerenciar pedidos, cupons e clientes.
- Integração com a **API do Asaas** para gerenciar clientes e pagamentos.
- Webhooks para receber atualizações sobre **pedidos do Woocommerce**.

## Pré-requisitos

Antes de rodar o projeto, você precisará de:

- Python 3.9 ou superior
- MySQL 5.7 ou superior
- Conta no **Woocommerce** (para integrar a API)
- Conta no **Asaas** (para integrar o gateway de pagamento)

## Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/RoberttWallker/portfolio_licensing_app.git
   cd portfolio_licensing_app
   ```

2. Crie e ative um ambiente virtual (recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Linux/Mac
   .\venv\Scripts\activate   # No Windows
   ```

3. Instale as dependências do projeto:
   ```bash
   pip install -r requirements.txt
   ```

4. Crie as tabelas do banco de dados:
   # Antes configure seu banco de dados MySQL corretamente.
   ```bash
   python manage.py migrate
   ```

5. Configure as variáveis de ambiente:
   - No arquivo `settings.py`, você precisa definir as credenciais para as APIs do **Woocommerce** e do **Asaas**:
     - **WC_CONSUMER_KEY**: Sua chave de consumidor do Woocommerce.
     - **WC_CONSUMER_SECRET**: Seu segredo de consumidor do Woocommerce.
     - **ASAAS_API_KEY**: Sua chave de API do Asaas.
   
6. (Opcional) Se precisar de um banco de dados diferente, altere as configurações do banco de dados no arquivo `settings.py`:
   - **NAME**: O nome do seu banco de dados.
   - **USER**: O usuário do banco de dados.
   - **PASSWORD**: A senha do banco de dados.

7. Crie um superusuário para acessar o painel administrativo:
   ```bash
   python manage.py createsuperuser
   ```

## Rodando o Projeto

1. Para rodar o servidor de desenvolvimento do Django:
   ```bash
   python manage.py runserver
   ```

2. Acesse o painel administrativo em: [http://127.0.0.1:8000/admin]

## Webhooks

Este projeto também possui integração com webhooks para os pedidos do Woocommerce.

- **Webhook Orders**: O segredo do webhook deve ser configurado em `WEBHOOK_ORDERS_SECRETS` no arquivo `settings.py`.
  **Para outros webhooks, crie uma variável em settings.py apontando para a nova lista de Secrets(Ex: CUSTOMERS)**

## Configurações Importantes

- **SECRET_KEY**: A chave secreta do Django deve ser gerada e mantida em segurança, especialmente em produção.
- **DEBUG**: O modo `DEBUG` deve ser desabilitado em produção, alterando para `False` e configurando as variáveis de ambiente adequadas.

## Banco de Dados

Este projeto utiliza o banco de dados **MySQL**. Certifique-se de que o MySQL está instalado e em execução antes de rodar o projeto. Configure as credenciais corretamente em `settings.py`.

## Contribuindo

1. Faça um fork do repositório.
2. Crie uma branch para a sua feature (`git checkout -b feature/nome-da-feature`).
3. Commit suas alterações (`git commit -am 'Adicionando nova feature'`).
4. Push para a branch (`git push origin feature/nome-da-feature`).
5. Abra um pull request.

## Licença

Este projeto está licenciado sob a [Licença MIT](LICENSE).

## Autores

- [RoberttWallker](https://github.com/RoberttWallker)
