# Generated by Django 2.0 on 2018-08-17 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demands', '0011_auto_20180818_0016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='approve_rejection',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
