# Generated by Django 4.0 on 2022-11-24 01:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('device', '0006_alter_rawdata_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rawdata',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 24, 8, 9, 3, 24916)),
        ),
    ]
