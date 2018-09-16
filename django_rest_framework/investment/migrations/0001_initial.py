# Generated by Django 2.1.1 on 2018-09-16 13:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Investment',
            fields=[
                ('date', models.DateField(default=datetime.date.today, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=128)),
                ('body', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('publishing', models.BooleanField(default=True)),
            ],
        ),
    ]
