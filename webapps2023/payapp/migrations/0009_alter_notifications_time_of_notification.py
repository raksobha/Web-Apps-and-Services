# Generated by Django 4.2 on 2023-05-02 23:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payapp', '0008_alter_notifications_time_of_notification_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notifications',
            name='time_of_notification',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 2, 23, 50, 51, 661207, tzinfo=datetime.timezone.utc)),
        ),
    ]
