# Generated by Django 4.2.4 on 2023-08-21 19:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('document_id', models.CharField(max_length=15, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('phone', models.CharField(max_length=10)),
                ('address', models.CharField(blank=True, max_length=70, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DocumentType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=70)),
                ('brand', models.CharField(blank=True, max_length=20, null=True)),
                ('reference', models.CharField(blank=True, max_length=60, null=True)),
                ('stock', models.IntegerField(default=0)),
                ('is_service', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='SaleType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Tax',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('percentage', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
        migrations.CreateModel(
            name='Return',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('reason', models.CharField(max_length=50)),
                ('return_date', models.DateTimeField(auto_now_add=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='point_of_sales.item')),
            ],
        ),
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('document_id', models.CharField(max_length=15)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('phone', models.CharField(max_length=10)),
                ('address', models.CharField(blank=True, max_length=70, null=True)),
                ('document_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='point_of_sales.documenttype')),
            ],
        ),
        migrations.CreateModel(
            name='Output',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('reason', models.CharField(max_length=50)),
                ('departure_date', models.DateTimeField(auto_now_add=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='point_of_sales.item')),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='provider',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='point_of_sales.provider'),
        ),
        migrations.AddField(
            model_name='item',
            name='tax',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='point_of_sales.tax'),
        ),
        migrations.CreateModel(
            name='InvoiceHeader',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subtotal', models.DecimalField(decimal_places=2, max_digits=12)),
                ('total_tax', models.DecimalField(decimal_places=2, max_digits=12)),
                ('discount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('total', models.DecimalField(decimal_places=2, max_digits=12)),
                ('paid', models.DecimalField(decimal_places=2, max_digits=12)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='point_of_sales.customer')),
                ('payment_method', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='point_of_sales.paymentmethod')),
                ('sales_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='point_of_sales.saletype')),
                ('user_created', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_created', to=settings.AUTH_USER_MODEL)),
                ('user_updated', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_updated', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='InvoiceDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('price', models.DecimalField(decimal_places=2, max_digits=12)),
                ('tax', models.DecimalField(decimal_places=2, max_digits=3)),
                ('discount', models.DecimalField(decimal_places=2, max_digits=3)),
                ('invoice_header', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='point_of_sales.invoiceheader')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='point_of_sales.item')),
            ],
        ),
        migrations.CreateModel(
            name='Input',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('purchase_order', models.CharField(max_length=12)),
                ('date_of_entry', models.DateTimeField(auto_now_add=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='point_of_sales.item')),
            ],
        ),
        migrations.AddField(
            model_name='customer',
            name='document_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='point_of_sales.documenttype'),
        ),
        migrations.AddConstraint(
            model_name='provider',
            constraint=models.UniqueConstraint(fields=('document_type', 'document_id'), name='unique_provide_document_type_and_id'),
        ),
        migrations.AddConstraint(
            model_name='customer',
            constraint=models.UniqueConstraint(condition=models.Q(('document_id__isnull', False)), fields=('document_type', 'document_id'), name='unique_customer_document_type_and_id'),
        ),
    ]
