# Generated by Django 3.2.21 on 2023-09-11 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tourism', '0047_auto_20230824_1635'),
    ]

    operations = [
        migrations.AlterField(
            model_name='touristiceventorganizer',
            name='label',
            field=models.CharField(max_length=256, verbose_name='Label'),
        ),
    ]