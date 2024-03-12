# Generated by Django 4.2.4 on 2024-03-07 21:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0001_initial'),
        ('point_of_sales', '0022_remove_customer_document_type_remove_input_item_and_more'),
        ('products_and_services', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoicedetail',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='item', to='products_and_services.item'),
        ),
        migrations.AlterField(
            model_name='invoiceheader',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer', to='customers.customer', verbose_name='Cliente'),
        ),
        migrations.AlterField(
            model_name='quotationdetail',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quotation_item', to='products_and_services.item'),
        ),
        migrations.AlterField(
            model_name='quotationheader',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quotation_customer', to='customers.customer', verbose_name='Cliente'),
        ),
        migrations.DeleteModel(
            name='Customer',
        ),
        migrations.DeleteModel(
            name='Input',
        ),
        migrations.DeleteModel(
            name='Item',
        ),
        migrations.DeleteModel(
            name='Output',
        ),
        migrations.DeleteModel(
            name='Payment',
        ),
        migrations.DeleteModel(
            name='Provider',
        ),
        migrations.DeleteModel(
            name='Return',
        ),
    ]