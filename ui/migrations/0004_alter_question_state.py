# Generated by Django 4.2.5 on 2023-11-26 01:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ui', '0003_rename_anwer_question_answer_alter_question_question'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='state',
            field=models.CharField(choices=[('new', 'new'), ('finished', 'finished'), ('unfinished', 'unfinished'), ('failed', 'failed')], default='new'),
        ),
    ]
