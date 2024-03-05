# Generated by Django 3.2.21 on 2023-12-06 16:27

import datetime
from django.db import migrations, models


def copy_date_into_begin_date(apps, schema_editor):
    # Get maintenance models to copy date filed into begin_date
    Intervention = apps.get_model('maintenance', 'Intervention')

    for inter in Intervention.objects.all():
        inter.begin_date = inter.date
        inter.save()


class Migration(migrations.Migration):

    dependencies = [
        ('maintenance', '0023_intervention_access'),
    ]

    operations = [
        migrations.AddField(
            model_name='intervention',
            name='begin_date',
            field=models.DateField(default=datetime.datetime.now, verbose_name='Begin date'),
        ),
        migrations.AddField(
            model_name='intervention',
            name='end_date',
            field=models.DateField(blank=True, null=True, verbose_name='End date'),
        ),
        migrations.RunPython(copy_date_into_begin_date, reverse_code=migrations.RunPython.noop),
    ]