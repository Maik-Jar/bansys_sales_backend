# Generated by Django 4.2.4 on 2023-08-23 03:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('point_of_sales', '0003_item_price_alter_invoicedetail_invoice_header_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='documenttype',
            name='status',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='invoiceheader',
            name='status',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='item',
            name='status',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='paymentmethod',
            name='status',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='provider',
            name='status',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='receipt',
            name='status',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='saletype',
            name='status',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='tax',
            name='status',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
    ]
