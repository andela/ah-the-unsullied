# Generated by Django 2.1.4 on 2019-01-25 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0003_auto_20190125_1004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='average_rating',
            field=models.IntegerField(default=0),
        ),
    ]
