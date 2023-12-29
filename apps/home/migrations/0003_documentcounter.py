# Generated by Django 5.0 on 2023-12-27 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_alter_purchaseorder_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentCounter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document_type', models.CharField(blank=True, choices=[('ORDER', 'Order')], max_length=30, null=True)),
                ('document_number', models.IntegerField(blank=True, default=1, null=True)),
            ],
        ),
    ]
