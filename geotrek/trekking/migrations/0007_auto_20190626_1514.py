# Generated by Django 1.11.14 on 2019-06-26 13:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trekking', '0006_practice_mobile_color'),
    ]

    operations = [
        migrations.RenameField(
            model_name='practice',
            old_name='mobile_color',
            new_name='color',
        ),
    ]