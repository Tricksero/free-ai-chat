# Generated by Django 4.2.5 on 2023-12-29 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ui', '0008_supported_api_type_alter_conversation_title_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='languagemodel',
            name='common_name',
            field=models.CharField(max_length=30),
        ),
    ]
