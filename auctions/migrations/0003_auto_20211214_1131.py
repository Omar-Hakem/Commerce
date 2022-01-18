# Generated by Django 3.2.7 on 2021-12-14 09:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_bid_category_comment_listing'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='listing',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='user',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='categories',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='user',
        ),
        migrations.DeleteModel(
            name='Bid',
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
        migrations.DeleteModel(
            name='Listing',
        ),
    ]
