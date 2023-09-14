# Generated by Django 4.2.4 on 2023-09-06 14:58

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("point_of_sales", "0008_alter_sequencereceipt_sequence"),
    ]

    operations = [
        migrations.AddField(
            model_name="sequencereceipt",
            name="date_created",
            field=models.DateTimeField(auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="sequencereceipt",
            name="status",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="sequencereceipt",
            name="to_reuse",
            field=models.BooleanField(default=False, editable=False),
        ),
        migrations.AlterField(
            model_name="invoiceheader",
            name="number",
            field=models.CharField(editable=False, max_length=12, unique=True),
        ),
        migrations.AlterField(
            model_name="invoiceheader",
            name="status",
            field=models.BooleanField(default=True, editable=False),
        ),
    ]
