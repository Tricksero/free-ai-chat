# Generated by Django 4.2.5 on 2023-12-28 13:42

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('ui', '0005_question_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
