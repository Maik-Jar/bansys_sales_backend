# Generated by Django 4.2.4 on 2024-03-08 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("customers", "0001_initial"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="customer",
            name="unique_customer_document_type_and_id",
        ),
        migrations.AddConstraint(
            model_name="customer",
            constraint=models.UniqueConstraint(
                condition=models.Q(("document_id__isnull", False)),
                fields=("document_type", "document_id"),
                name="unique_customer_document_id_and_document_type",
            ),
        ),
    ]