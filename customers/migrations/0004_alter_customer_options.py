# Generated by Django 4.2.4 on 2024-03-08 14:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0003_alter_customer_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customer',
            options={'verbose_name': 'Cliente', 'verbose_name_plural': 'Clientes'},
        ),
    ]
