# Generated by Django 2.1.2 on 2019-07-25 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feivs2019AccountManager', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mytweets',
            name='reply_to_id',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
