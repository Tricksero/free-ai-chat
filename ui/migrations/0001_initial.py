# Generated by Django 4.2.5 on 2023-10-18 20:28

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Conversation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('title', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('json', models.JSONField()),
                ('model', models.CharField(max_length=255)),
                ('state', models.CharField(choices=[('finished', 'finished'), ('unfinished', 'unfinished'), ('failed', 'failed')])),
                ('conversation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ui.conversation')),
            ],
        ),
    ]
