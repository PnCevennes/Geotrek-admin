# Generated by Django 1.11.14 on 2019-03-06 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signage', '0005_logentry_signage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blade',
            name='number',
            field=models.CharField(db_column='numero', max_length=250, verbose_name='Blade Number'),
        ),
    ]