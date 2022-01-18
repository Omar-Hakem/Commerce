# Generated by Django 3.2.7 on 2021-12-15 03:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_auto_20211215_0020'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='url',
            new_name='image_url',
        ),
        migrations.RenameField(
            model_name='listing',
            old_name='name',
            new_name='title',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='categories',
        ),
        migrations.AddField(
            model_name='listing',
            name='category',
            field=models.ManyToManyField(blank=True, to='auctions.Category'),
        ),
    ]