# Generated by Django 2.0 on 2018-08-16 13:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demands', '0004_auto_20180816_1557'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journal_entry',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
