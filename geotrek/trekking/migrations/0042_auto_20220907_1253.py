# Generated by Django 3.1.14 on 2022-09-07 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trekking', '0041_auto_20220304_1442'),
    ]

    operations = [
        migrations.AddField(
            model_name='poi',
            name='provider',
            field=models.CharField(blank=True, db_index=True, max_length=1024, verbose_name='Provider'),
        ),
        migrations.AddField(
            model_name='service',
            name='provider',
            field=models.CharField(blank=True, db_index=True, max_length=1024, verbose_name='Provider'),
        ),
        migrations.AddField(
            model_name='trek',
            name='provider',
            field=models.CharField(blank=True, db_index=True, max_length=1024, verbose_name='Provider'),
        ),
    ]
