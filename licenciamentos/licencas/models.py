import re
from django.db import models
from django.utils import timezone
import jwt
from datetime import timedelta
from django.conf import settings
from django.utils.timezone import now


class Cliente(models.Model):
    asaas_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    tipo_pessoa = models.CharField(
        max_length=10,
        null=False,
        blank=False,
        choices= [
        ('FISICA', 'Pessoa Física'),
        ('JURIDICA', 'Pessoa Jurídica'),
        ],
        default='FISICA')
    nome = models.CharField(max_length=255, null=False, blank=False)
    razao_social = models.CharField(max_length=255, null=True, blank=True)
    cpf_cnpj = models.CharField(max_length=18, unique=True, null=True, blank=True)
    inscricao_municipal = models.CharField(max_length=50, null=True, blank=True)
    inscricao_estadual = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    telefone_1 = models.CharField(max_length=21, null=True, blank=True)
    telefone_2 = models.CharField(max_length=21, null=True, blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_ult_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.tipo_pessoa == "FISICA":
            cliente = f"""
{self.nome} (ID interno: {self.id}, ID Asaas: {self.asaas_id})
CPF: {self.cpf_cnpj}
E-mail: {self.email}
Telefone: {self.telefone}
Celular: {self.telefone_celular}
Data Criação: {self.data_criacao}
"""
        if self.tipo_pessoa == "JURIDICA":
            cliente = f"""
{self.nome} (ID interno: {self.id}, ID Asaas: {self.asaas_id})
Razão Social: {self.razao_social}
CNPJ: {self.cpf_cnpj}
E-mail: {self.email}
Telefone: {self.telefone}
Celular: {self.telefone_celular}
Data Criação: {self.data_criacao}
"""
        else:
            cliente = f"{self.nome} (ID interno: {self.id}) - Tipo desconhecido"

        return cliente
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.data_criacao:
            self.data_criacao = timezone.now() - timedelta(hours=3)  # Definindo o horário manualmente.
            # Atualizar a data_criacao no banco de dados após o primeiro save
            Cliente.objects.filter(pk=self.pk).update(data_criacao=self.data_criacao)
    
class Fornecedor(models.Model):
    #Campos gerais
    nome = models.CharField(max_length=255)
    razao_social = models.CharField(max_length=255, blank=True, null=True)
    tipo_pessoa = models.CharField(
        max_length=10,
        choices=[
        ('FISICA', 'Pessoa Física'),
        ('JURIDICA', 'Pessoa Jurídica'),
        ],
        default='JURIDICA')
    cpf_cnpj = models.CharField(max_length=18, unique=True)
    email = models.EmailField(blank=True, null=True)
    telefone_1 = models.CharField(max_length=21, blank=True, null=True)
    telefone_2 = models.CharField(max_length=21, blank=True, null=True)

    #Campos bancários
    banco = models.CharField(max_length=100, blank=True, null=True)
    agencia = models.CharField(max_length=50, blank=True, null=True)
    conta_corrente = models.CharField(max_length=50, blank=True, null=True)
    pix_chave = models.CharField(max_length=255, blank=True, null=True)
    forma_pagamento = models.CharField(max_length=50, blank=True, null=True)
    prazo_pagamento = models.IntegerField(default=30)  # Prazo em dias
    limite_credito = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    desconto_maximo = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    #Campos fiscais
    inscricao_estadual = models.CharField(max_length=50, blank=True, null=True)
    inscricao_municipal = models.CharField(max_length=50, blank=True, null=True)
    cnae = models.CharField(max_length=100, blank=True, null=True)  # Código de Atividade Econômica
    crt = models.CharField(max_length=50, blank=True, null=True)  # Código de Regime Tributário
    pis = models.CharField(max_length=20, blank=True, null=True)  # PIS
    cofins = models.CharField(max_length=20, blank=True, null=True)  # COFINS
    cst_icms = models.CharField(max_length=10, blank=True, null=True)  # Código de Situação Tributária (ICMS)
    iss = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # ISS (Imposto Sobre Serviços)
    regime_pis_cofins = models.CharField(max_length=20, blank=True, null=True)  # Regime de Apuração (PIS/COFINS)
    responsabilidade_tributaria = models.CharField(max_length=50, blank=True, null=True)  # Substituição Tributária
    emite_nfe = models.BooleanField(default=False)  # Emite NF-e? (Nota Fiscal Eletrônica)

    #Campos auxiliares
    ativo = models.BooleanField(default=True)
    categoria = models.CharField(max_length=100, blank=True, null=True)
    observacoes = models.TextField(blank=True, null=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    data_ult_atualizacao = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.nome
      
class Endereco(models.Model):
    cliente = models.ForeignKey(Cliente, null=True, blank=True, on_delete=models.PROTECT)
    fornecedor = models.ForeignKey(Fornecedor, null=True, blank=True, on_delete=models.PROTECT)
    logradouro = models.CharField(max_length=255, null=False, blank=False)
    numero = models.IntegerField(null=True, blank=True)
    complemento = models.CharField(max_length=255, null=True, blank=True)
    bairro = models.CharField(max_length=255, null=False, blank=False)
    cep = models.CharField(max_length=8, null=False, blank=False)
    cidade = models.CharField(max_length=255, null=False, blank=False)
    estado = models.CharField(max_length=2, null=False, blank=False)
    pais = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return f"{self.logradouro}, {self.numero} - {self.bairro}, {self.cidade}/{self.estado}, {self.pais} - CEP: {self.cep}"
    
    def save(self, *args, **kwargs):
        # Atualizar data_ult_atualizacao do cliente, se existir
        if self.cliente:
            self.cliente.data_ult_atualizacao = now()
            self.cliente.save(update_fields=['data_ult_atualizacao'])
        
        # Atualizar data_ult_atualizacao do fornecedor, se existir
        if self.fornecedor:
            self.fornecedor.data_ult_atualizacao = now()
            self.fornecedor.save(update_fields=['data_ult_atualizacao'])


        super().save(*args, **kwargs)

class Licenca(models.Model):
    licenca_id = models.CharField(max_length=100, unique=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    status = models.CharField(
        max_length=20,
        choices=[
            ('ativa', 'Ativa'),
            ('inativa', 'Inativa'),
            ('cancelada', 'Cancelada')
            ]
        )
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_expiracao = models.DateTimeField(null=True, blank=True)
    jwt_token = models.CharField(max_length=255)
    tipo_licenca = models.CharField(
        max_length=10,
        choices=[
            ('diaria', 'Diária'),
            ('mensal', 'Mensal'),
            ('semestral', 'Semestral'),
            ('anual', 'Anual')
            ],
            default='mensal'
        )

    def save(self, *args, **kwargs):
        # Gerar licenca_id automaticamente
        if not self.licenca_id:
            last_licenca = Licenca.objects.filter(licenca_id__regex=r'^LDPE\d{6}$').order_by('-licenca_id').first()  # Buscar pelo ID numérico
            if last_licenca:
                match = re.match(r'LDPE(\d+)', last_licenca.licenca_id)
                next_number = int(match.group(1)) + 1 if match else 1
            else:
                next_number = 1

            self.licenca_id = f'LDPE{next_number:06d}'
 
        super().save(*args, **kwargs)

        if self.data_criacao:
            self.data_criacao = timezone.now() - timedelta(hours=3)  # Definindo o horário manualmente.
            # Atualizar a data_criacao no banco de dados após o primeiro save
            Licenca.objects.filter(pk=self.pk).update(data_criacao=self.data_criacao)

        if not self.data_expiracao or self.data_expiracao == None:
            if self.tipo_licenca == 'diaria':
                self.data_expiracao = self.data_criacao + timedelta(days=1)
            elif self.tipo_licenca == 'mensal':
                self.data_expiracao = self.data_criacao + timedelta(days=30)
            elif self.tipo_licenca == 'semestral':
                self.data_expiracao = self.data_criacao + timedelta(days=180)
            elif self.tipo_licenca == 'anual':
                self.data_expiracao = self.data_criacao + timedelta(days=365)

            # Atualiza apenas o campo data_expiracao sem chamar save() novamente
            Licenca.objects.filter(pk=self.pk).update(data_expiracao=self.data_expiracao)

        if not self.jwt_token:
            payload = {
                "cliente": self.cliente.id,
                "data_criacao": self.data_criacao.isoformat(),
                "licenca_id": self.licenca_id,
            }

            self.jwt_token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

            Licenca.objects.filter(pk=self.pk).update(jwt_token=self.jwt_token)

    def __str__(self):
        return f"Licença {self.licenca_id} para cliente {self.cliente.id} (Status: {self.status}) (TOKEN: {self.jwt_token})"
    
    @classmethod
    def verificar_jwt(cls, token):
        try:
            # Decodifica o token usando a chave secreta
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            
            # Verifica os dados contidos no payload
            cliente_id = payload.get("cliente")
            data_criacao = payload.get("data_criacao")
            licenca_id = payload.get("licenca_id")
            
            if not cliente_id or not data_criacao or not licenca_id:
                raise jwt.InvalidTokenError("Token inválido, informações faltando.")
            
            # Verifica se a licença existe e está ativa
            licenca_obj = cls.objects.filter(licenca_id=licenca_id).first()
            if not licenca_obj:
                raise jwt.InvalidTokenError("Licença não encontrada.")
            
            # Verifica se o cliente associado à licença é o mesmo do token
            if licenca_obj.cliente.id != cliente_id:
                raise jwt.InvalidTokenError("Cliente não corresponde ao token.")
            
            return licenca_obj.status  # Retorna os dados do payload se tudo estiver ok
        
        except jwt.InvalidTokenError as e:
            raise jwt.InvalidTokenError(f"Token inválido: {str(e)}")

class Produtos(models.Model):
    # Dados gerais
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.PROTECT)
    nome = models.CharField(max_length=255, unique=True, null=True, blank=True)
    descricao = models.CharField(max_length=255, null=True, blank=True)
    sku = models.CharField(max_length=11, unique=True, null=True, blank=True)
    grupo = models.CharField(max_length=7, choices=[('digital', 'Digital'), ('fisico', 'Físico')], default='digital')
    tipo = models.CharField(max_length=100, null=True, blank=True)
    marca = models.CharField(max_length=100, null=True, blank=True)
    versao = models.CharField(max_length=100, null=True, blank=True)
    variacao = models.CharField(max_length=100, null=True, blank=True)
    tags = models.CharField(max_length=255, null=True, blank=True)
    observacoes = models.TextField(null=True, blank=True)

    # Dados de valores
    valor_venda = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)
    valor_custo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)
    markup = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)
    max_desconto = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # Dados Auxiliares
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

