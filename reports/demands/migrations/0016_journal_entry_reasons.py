# Generated by Django 2.0 on 2018-08-24 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demands', '0015_auto_20180823_1641'),
    ]

    operations = [
        migrations.AddField(
            model_name='journal_entry',
            name='reasons',
            field=models.CharField(max_length=255, null=True),
        ),
    ]