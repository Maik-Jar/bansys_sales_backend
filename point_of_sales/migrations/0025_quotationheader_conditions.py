# Generated by Django 4.2.4 on 2024-05-29 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master_data', '0003_alter_condition_options'),
        ('point_of_sales', '0024_remove_invoiceheader_avance_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='quotationheader',
            name='conditions',
            field=models.ManyToManyField(null=True, to='master_data.condition'),
        ),
    ]
