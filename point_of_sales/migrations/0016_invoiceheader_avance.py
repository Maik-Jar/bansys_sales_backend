# Generated by Django 4.2.4 on 2024-02-01 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('point_of_sales', '0015_alter_company_options_alter_customer_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoiceheader',
            name='avance',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=12, verbose_name='abono'),
        ),
    ]