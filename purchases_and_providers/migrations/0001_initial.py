# Generated by Django 4.2.4 on 2024-03-07 21:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('master_data', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Nombre')),
                ('document_id', models.CharField(max_length=15, verbose_name='No. Documento')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Correo')),
                ('phone', models.CharField(max_length=10, verbose_name='Teléfono')),
                ('address', models.CharField(blank=True, max_length=70, null=True, verbose_name='Dirección')),
                ('status', models.BooleanField(default=True, verbose_name='Estatus')),
                ('document_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='master_data.documenttype', verbose_name='Tipo de documento')),
            ],
            options={
                'verbose_name': 'Proveedor',
                'verbose_name_plural': 'Proveedores',
            },
        ),
        #migrations.AddConstraint(
        #    model_name='provider',
        #    constraint=models.UniqueConstraint(fields=('document_type', 'document_id'), name='unique_provide_document_type_and_id'),
        #),
    ]
