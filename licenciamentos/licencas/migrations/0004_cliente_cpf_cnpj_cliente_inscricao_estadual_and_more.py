# Generated by Django 5.1.6 on 2025-02-25 18:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('licencas', '0003_rename_wordpress_id_cliente_asaas_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='cpf_cnpj',
            field=models.CharField(blank=True, max_length=18, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='cliente',
            name='inscricao_estadual',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='cliente',
            name='inscricao_municipal',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='cliente',
            name='razao_social',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='cliente',
            name='telefone',
            field=models.CharField(blank=True, max_length=21, null=True),
        ),
        migrations.AddField(
            model_name='cliente',
            name='telefone_celular',
            field=models.CharField(blank=True, max_length=21, null=True),
        ),
        migrations.AddField(
            model_name='cliente',
            name='tipo_pessoa',
            field=models.CharField(default='FISICA', max_length=10),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.CreateModel(
            name='Endereco',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logradouro', models.CharField(max_length=255)),
                ('numero', models.IntegerField(blank=True, null=True)),
                ('complemento', models.CharField(blank=True, max_length=255, null=True)),
                ('bairro', models.CharField(max_length=255)),
                ('cep', models.CharField(max_length=8)),
                ('cidade', models.CharField(max_length=255)),
                ('estado', models.CharField(max_length=2)),
                ('pais', models.CharField(max_length=255)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='licencas.cliente')),
            ],
        ),
    ]
