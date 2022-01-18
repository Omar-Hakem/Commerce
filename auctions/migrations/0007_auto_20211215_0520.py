# Generated by Django 3.2.7 on 2021-12-15 03:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_auto_20211215_0515'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='price',
        ),
        migrations.AddField(
            model_name='listing',
            name='currentBid',
            field=models.DecimalField(decimal_places=2, max_digits=10000, null=True),
        ),
        migrations.AlterField(
            model_name='listing',
            name='startingBid',
            field=models.DecimalField(decimal_places=2, max_digits=10000, null=True),
        ),
    ]