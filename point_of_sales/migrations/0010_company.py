# Generated by Django 4.2.4 on 2023-09-08 18:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('point_of_sales', '0009_sequencereceipt_date_created_sequencereceipt_status_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('document_id', models.CharField(max_length=15, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('phone', models.CharField(max_length=10)),
                ('address', models.CharField(blank=True, max_length=70, null=True)),
                ('logo', models.ImageField(blank=True, upload_to='')),
                ('document_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company_document_type', to='point_of_sales.documenttype')),
            ],
        ),
    ]
