# Generated by Django 2.1.4 on 2019-01-25 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='average_rating',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=2),
        ),
    ]
