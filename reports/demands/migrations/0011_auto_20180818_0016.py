# Generated by Django 2.0 on 2018-08-17 21:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('demands', '0010_approve_rejection_journal_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='approve_rejection',
            old_name='notes',
            new_name='reasons',
        ),
    ]
