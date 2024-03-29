# Generated by Django 4.2 on 2023-05-02 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_currencyconversion_start_currency_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currencyconversion',
            name='start_currency',
            field=models.CharField(choices=[('USD', 'USD'), ('EUR', 'EUR'), ('GBP', 'GBP')], max_length=3),
        ),
        migrations.AlterField(
            model_name='currencyconversion',
            name='target_currency',
            field=models.CharField(choices=[('USD', 'USD'), ('EUR', 'EUR'), ('GBP', 'GBP')], max_length=3),
        ),
    ]
