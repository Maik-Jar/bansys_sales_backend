# Generated by Django 4.2.4 on 2024-03-07 21:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('inventory', '0002_initial'),
        ('purchases_and_providers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='input',
            name='provider',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='purchases_and_providers.provider', verbose_name='Proveedor'),
        ),
    ]
