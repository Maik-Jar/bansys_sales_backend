# Generated by Django 4.2.4 on 2024-02-22 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('point_of_sales', '0019_invoicedetail_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='discount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Descuento'),
        ),
    ]
