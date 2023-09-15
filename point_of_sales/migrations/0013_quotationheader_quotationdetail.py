# Generated by Django 4.2.4 on 2023-09-14 17:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('point_of_sales', '0012_remove_invoiceheader_receipt_type_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuotationHeader',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(editable=False, max_length=12, unique=True)),
                ('discount', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('comment', models.CharField(blank=True, max_length=400, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('status', models.BooleanField(default=True, editable=False)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='quotation_customer', to='point_of_sales.customer')),
                ('sales_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='point_of_sales.saletype')),
                ('user_created', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='quotation_user_created', to=settings.AUTH_USER_MODEL)),
                ('user_updated', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='quotation_user_updated', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='QuotationDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('price', models.DecimalField(decimal_places=2, max_digits=12)),
                ('tax', models.DecimalField(decimal_places=2, max_digits=12)),
                ('discount', models.DecimalField(decimal_places=2, max_digits=3)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quotation_item', to='point_of_sales.item')),
                ('quotation_header', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quotation_detail', to='point_of_sales.quotationheader')),
            ],
        ),
    ]