# Generated by Django 3.1.14 on 2022-09-07 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('infrastructure', '0030_auto_20220314_1429'),
    ]

    operations = [
        migrations.AddField(
            model_name='infrastructure',
            name='provider',
            field=models.CharField(blank=True, db_index=True, max_length=1024, verbose_name='Provider'),
        ),
    ]
