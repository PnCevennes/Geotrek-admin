# Generated by Django 3.1.3 on 2020-12-04 09:33

from django.conf import settings
import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion
import geotrek.common.mixins


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authent', '0005_remove_userprofile_language'),
    ]

    operations = [
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_insert', models.DateTimeField(auto_now_add=True, verbose_name="Date d'insertion")),
                ('date_update', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Date de modification')),
                ('geom', django.contrib.gis.db.models.fields.GeometryField(srid=settings.SRID, verbose_name='Location')),
                ('name', models.CharField(max_length=128, verbose_name='Name')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('eid', models.CharField(blank=True, max_length=1024, null=True, verbose_name='External id')),
                ('structure', models.ForeignKey(default=settings.DEFAULT_STRUCTURE_PK, on_delete=django.db.models.deletion.CASCADE, to='authent.structure', verbose_name='Related structure')),
            ],
            options={
                'verbose_name': 'Site',
                'verbose_name_plural': 'Sites',
                'ordering': ('name',),
            },
            bases=(geotrek.common.mixins.AddPropertyMixin, models.Model),
        ),
    ]
