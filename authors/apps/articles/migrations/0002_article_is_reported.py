# Generated by Django 2.1.4 on 2019-02-05 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='is_reported',
            field=models.BooleanField(default=False),
        ),
    ]