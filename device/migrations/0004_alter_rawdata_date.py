# Generated by Django 4.0 on 2022-11-12 02:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('device', '0003_alter_rawdata_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rawdata',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 12, 9, 15, 24, 257659)),
        ),
    ]