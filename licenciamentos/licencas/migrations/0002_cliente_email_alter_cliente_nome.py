# Generated by Django 5.1.6 on 2025-02-20 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('licencas', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='email',
            field=models.EmailField(max_length=254, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='nome',
            field=models.CharField(max_length=255),
        ),
    ]
