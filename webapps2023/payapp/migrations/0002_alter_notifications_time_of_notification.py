# Generated by Django 4.2 on 2023-05-02 03:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notifications',
            name='time_of_notification',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 2, 3, 18, 2, 657324, tzinfo=datetime.timezone.utc)),
        ),
    ]