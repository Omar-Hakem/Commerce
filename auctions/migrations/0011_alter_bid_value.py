# Generated by Django 3.2.7 on 2022-01-03 01:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_watchlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='value',
            field=models.DecimalField(decimal_places=2, max_digits=10000, null=True),
        ),
    ]
