# Generated by Django 2.1.4 on 2019-01-18 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0006_auto_20190117_0819'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
    ]