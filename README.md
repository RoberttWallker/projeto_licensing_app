# projeto_licensing_app
##Este projeto foi feito para enriquecer o portfólio pessoal, após o uso em ambiente real.
Este é um projeto Django para criação e gerenciamento de **licenças** com integração ao **Woocommerce** e ao **gateway de pagamentos Asaas**. O aplicativo tem como objetivo facilitar a gestão de licenças para um portfólio de produtos, com funcionalidades para criação de pedidos, cupons, clientes e integração com o sistema de pagamento Asaas.

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python) | ![Django](https://img.shields.io/badge/Django-5.1-green?logo=django) | ![MySQL](https://img.shields.io/badge/MySQL-8.3-orange?logo=mysql) | ![WooCommerce](https://img.shields.io/badge/WooCommerce-API-purple?logo=woocommerce) | ![Asaas](https://img.shields.io/badge/Asaas-Payments-red) | | ![Requests](https://img.shields.io/badge/Requests-HTTP-blue?logo=python)


## Tecnologias

- Django 5.1.7
- MySQL
- API Woocommerce
- API Asaas
- Requests (para comunicação com APIs)

## Funcionalidades

- Criação e gerenciamento de **licenças**.
- Integração com a **API do Woocommerce** para gerenciar pedidos, cupons e clientes.
- Integração com a **API do Asaas** para gerenciar clientes e pagamentos.
- Webhooks para receber atualizações sobre **pedidos do Woocommerce**.

## Pré-requisitos

Antes de rodar o projeto, você precisará de:

- Python 3.12 ou superior
- MySQL 8.3.0 ou superior
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
   ##### * Antes configure seu banco de dados corretamente.
   altere as configurações do banco de dados no arquivo `settings.py`:
   
   - **ENGINE**: django.db.backends.aqui-o-dialect-do-sgbd. (Ex: mysql)
   - **NAME**: O nome do seu banco de dados.
   - **USER**: O usuário do banco de dados.
   - **PASSWORD**: A senha do banco de dados.
   - **HOST**: O host do banco de dados.
   - **PORT**: A porta que o banco de dados está usando.
   
   Execute o comando no terminal:
   ```bash
   python manage.py migrate # No Windows
   python3 manage.py migrate # No Linux
   ```

5. Configure as variáveis de ambiente:
   - No arquivo `settings.py`, você precisa definir as credenciais para as APIs do **Woocommerce** e do **Asaas**:
     - **WC_CONSUMER_KEY**: Sua chave de consumidor do Woocommerce.
     - **WC_CONSUMER_SECRET**: Seu segredo de consumidor do Woocommerce.
     - **ASAAS_API_KEY**: Sua chave de API do Asaas.
	 
6. Crie um superusuário para acessar o painel administrativo:
   ```bash
   python manage.py createsuperuser
   ```

## Rodando o Projeto

1. Para rodar o servidor de desenvolvimento do Django:
   ```bash
   python manage.py runserver 127.0.0.1:8000
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


## This project was created to enrich the personal portfolio, after being used in a real environment.
This is a Django project for creating and managing **licenses** with integration to **Woocommerce** and the **Asaas payment gateway**. The app aims to simplify license management for a product portfolio, with features for creating orders, coupons, customers, and integration with the Asaas payment system.

## Technologies

- Django 5.1.7
- MySQL
- Woocommerce API
- Asaas API
- Requests (for communication with APIs)

## Features

- Creation and management of **licenses**.
- Integration with the **Woocommerce API** to manage orders, coupons, and customers.
- Integration with the **Asaas API** to manage customers and payments.
- Webhooks to receive updates on **Woocommerce orders**.

## Prerequisites

Before running the project, you will need:

- Python 3.12 or higher
- MySQL 8.3.0 or higher
- Woocommerce account (to integrate the API)
- Asaas account (to integrate the payment gateway)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/RoberttWallker/portfolio_licensing_app.git
   cd portfolio_licensing_app
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Linux/Mac
   .env\Scriptsctivate   # On Windows
   ```

3. Install the project dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create the database tables:
   ##### *Beforehand, configure your database properly.*
   Modify the database settings in the `settings.py` file:
   
   - **ENGINE**: django.db.backends.<your-db-dialect>. (e.g., mysql)
   - **NAME**: The name of your database.
   - **USER**: The database user.
   - **PASSWORD**: The database password.
   - **HOST**: The database host.
   - **PORT**: The port the database is using.
   
   Run the command in the terminal:
   ```bash
   python manage.py migrate # On Windows
   python3 manage.py migrate # On Linux
   ```

5. Configure the environment variables:
   - In the `settings.py` file, you need to define the credentials for the **Woocommerce** and **Asaas** APIs:
     - **WC_CONSUMER_KEY**: Your Woocommerce consumer key.
     - **WC_CONSUMER_SECRET**: Your Woocommerce consumer secret.
     - **ASAAS_API_KEY**: Your Asaas API key.
     
6. Create a superuser to access the admin panel:
   ```bash
   python manage.py createsuperuser
   ```

## Running the Project

1. To run the Django development server:
   ```bash
   python manage.py runserver 127.0.0.1:8000
   ```

2. Access the admin panel at: [http://127.0.0.1:8000/admin]

## Webhooks

This project also integrates with webhooks for Woocommerce orders.

- **Webhook Orders**: The webhook secret must be configured in `WEBHOOK_ORDERS_SECRETS` in the `settings.py` file.
  
  **For other webhooks, create a variable in settings.py pointing to the new list of Secrets (e.g., CUSTOMERS)**

## Important Settings

- **SECRET_KEY**: The Django secret key should be generated and kept secure, especially in production.
- **DEBUG**: The `DEBUG` mode should be disabled in production, set it to `False` and configure the appropriate environment variables.

## Database

This project uses the **MySQL** database. Ensure MySQL is installed and running before running the project. Configure the credentials correctly in `settings.py`.

## Contributing

1. Fork the repository.
2. Create a branch for your feature (`git checkout -b feature/feature-name`).
3. Commit your changes (`git commit -am 'Adding new feature'`).
4. Push to the branch (`git push origin feature/feature-name`).
5. Open a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Authors

- [RoberttWallker](https://github.com/RoberttWallker)
