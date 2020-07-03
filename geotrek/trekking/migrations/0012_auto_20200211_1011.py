# -*- coding: utf-8 -*-
# Generated by Django 1.11.27 on 2020-02-11 10:11
from __future__ import unicode_literals

import colorfield.fields
from django.conf import settings
import django.contrib.gis.db.models.fields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import geotrek.authent.models


class Migration(migrations.Migration):

    dependencies = [
        ('trekking', '0011_auto_20191210_0921'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='trek',
            options={'ordering': ('name',), 'verbose_name': 'Trek', 'verbose_name_plural': 'Treks'},
        ),
        migrations.AlterField(
            model_name='accessibility',
            name='name',
            field=models.CharField(max_length=128, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='difficultylevel',
            name='cirkwi_level',
            field=models.IntegerField(blank=True, help_text='Between 1 and 8', null=True, verbose_name='Cirkwi level'),
        ),
        migrations.AlterField(
            model_name='difficultylevel',
            name='difficulty',
            field=models.CharField(max_length=128, verbose_name='Difficulty level'),
        ),
        migrations.AlterField(
            model_name='poi',
            name='description',
            field=models.TextField(blank=True, help_text='History, details,  ...', verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='poi',
            name='eid',
            field=models.CharField(blank=True, max_length=1024, null=True, verbose_name='External id'),
        ),
        migrations.AlterField(
            model_name='poi',
            name='structure',
            field=models.ForeignKey(default=geotrek.authent.models.default_structure_pk, on_delete=django.db.models.deletion.CASCADE, to='authent.Structure', verbose_name='Related structure'),
        ),
        migrations.AlterField(
            model_name='poi',
            name='topo_object',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.Topology'),
        ),
        migrations.AlterField(
            model_name='poi',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pois', to='trekking.POIType', verbose_name='Type'),
        ),
        migrations.AlterField(
            model_name='poitype',
            name='label',
            field=models.CharField(max_length=128, verbose_name='Label'),
        ),
        migrations.AlterField(
            model_name='practice',
            name='color',
            field=colorfield.fields.ColorField(default='#444444', help_text='Color of the practice, only used in mobile.', max_length=18, verbose_name='Color'),
        ),
        migrations.AlterField(
            model_name='practice',
            name='distance',
            field=models.IntegerField(blank=True, help_text='Touristic contents and events will associate within this distance (meters)', null=True, verbose_name='Distance'),
        ),
        migrations.AlterField(
            model_name='practice',
            name='name',
            field=models.CharField(max_length=128, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='practice',
            name='order',
            field=models.IntegerField(blank=True, help_text='Alphabetical order if blank', null=True, verbose_name='Order'),
        ),
        migrations.AlterField(
            model_name='route',
            name='route',
            field=models.CharField(max_length=128, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='service',
            name='eid',
            field=models.CharField(blank=True, max_length=1024, null=True, verbose_name='External id'),
        ),
        migrations.AlterField(
            model_name='service',
            name='structure',
            field=models.ForeignKey(default=geotrek.authent.models.default_structure_pk, on_delete=django.db.models.deletion.CASCADE, to='authent.Structure', verbose_name='Related structure'),
        ),
        migrations.AlterField(
            model_name='service',
            name='topo_object',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.Topology'),
        ),
        migrations.AlterField(
            model_name='service',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='services', to='trekking.ServiceType', verbose_name='Type'),
        ),
        migrations.AlterField(
            model_name='servicetype',
            name='practices',
            field=models.ManyToManyField(blank=True, related_name='services', to='trekking.Practice', verbose_name='Practices'),
        ),
        migrations.AlterField(
            model_name='trek',
            name='access',
            field=models.TextField(blank=True, help_text='Best way to go', verbose_name='Access'),
        ),
        migrations.AlterField(
            model_name='trek',
            name='accessibilities',
            field=models.ManyToManyField(blank=True, related_name='treks', to='trekking.Accessibility', verbose_name='Accessibility'),
        ),
        migrations.AlterField(
            model_name='trek',
            name='advice',
            field=models.TextField(blank=True, help_text='Risks, danger, best period, ...', verbose_name='Advice'),
        ),
        migrations.AlterField(
            model_name='trek',
            name='advised_parking',
            field=models.CharField(blank=True, help_text='Where to park', max_length=128, verbose_name='Advised parking'),
        ),
        migrations.AlterField(
            model_name='trek',
            name='ambiance',
            field=models.TextField(blank=True, help_text='Main attraction and interest', verbose_name='Ambiance'),
        ),
        migrations.AlterField(
            model_name='trek',
            name='arrival',
            field=models.CharField(blank=True, help_text='Arrival description', max_length=128, verbose_name='Arrival'),
        ),
        migrations.AlterField(
            model_name='trek',
            name='departure',
            field=models.CharField(blank=True, help_text='Departure description', max_length=128, verbose_name='Departure'),
        ),
        migrations.AlterField(
            model_name='trek',
            name='description',
            field=models.TextField(blank=True, help_text='Complete description', verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='trek',
            name='description_teaser',
            field=models.TextField(blank=True, help_text='A brief summary (map pop-ups)', verbose_name='Description teaser'),
        ),
        migrations.AlterField(
            model_name='trek',
            name='difficulty',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='treks', to='trekking.DifficultyLevel', verbose_name='Difficulty'),
        ),
        migrations.AlterField(
            model_name='trek',
            name='disabled_infrastructure',
            field=models.TextField(blank=True, help_text='Any specific infrastructure', verbose_name='Disabled infrastructure'),
        ),
        migrations.AlterField(
            model_name='trek',
            name='duration',
            field=models.FloatField(blank=True, help_text='In hours (1.5 = 1 h 30, 24 = 1 day, 48 = 2 days)', null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Duration'),
        ),
        migrations.AlterField(
            model_name='trek',
            name='eid',
            field=models.CharField(blank=True, max_length=1024, null=True, verbose_name='External id'),
        ),
        migrations.AlterField(
            model_name='trek',
            name='eid2',
            field=models.CharField(blank=True, max_length=1024, null=True, verbose_name='Second external id'),
        ),
        migrations.AlterField(
            model_name='trek',
            name='information_desks',
            field=models.ManyToManyField(blank=True, help_text='Where to obtain information', related_name='treks', to='tourism.InformationDesk', verbose_name='Information desks'),
        ),
        migrations.AlterField(
            model_name='trek',
            name='is_park_centered',
            field=models.BooleanField(default=False, help_text='Crosses center of park', verbose_name='Is in the midst of the park'),
        ),
        migrations.AlterField(
            model_name='trek',
            name='networks',
            field=models.ManyToManyField(blank=True, help_text='Hiking networks', related_name='treks', to='trekking.TrekNetwork', verbose_name='Networks'),
        ),
        migrations.AlterField(
            model_name='trek',
            name='parking_location',
            field=django.contrib.gis.db.models.fields.PointField(blank=True, null=True, spatial_index=False, srid=settings.SRID, verbose_name='Parking location'),
        ),
        migrations.AlterField(
            model_name='trek',
            name='points_reference',
            field=django.contrib.gis.db.models.fields.MultiPointField(blank=True, null=True, spatial_index=False, srid=settings.SRID, verbose_name='Points of reference'),
        ),
        migrations.AlterField(
            model_name='trek',
            name='pois_excluded',
            field=models.ManyToManyField(blank=True, related_name='excluded_treks', to='trekking.POI', verbose_name='Excluded POIs'),
        ),
        migrations.AlterField(
            model_name='trek',
            name='portal',
            field=models.ManyToManyField(blank=True, related_name='treks', to='common.TargetPortal', verbose_name='Portal'),
        ),
        migrations.AlterField(
            model_name='trek',
            name='practice',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='treks', to='trekking.Practice', verbose_name='Practice'),
        ),
        migrations.AlterField(
            model_name='trek',
            name='public_transport',
            field=models.TextField(blank=True, help_text='Train, bus (see web links)', verbose_name='Public transport'),
        ),
        migrations.AlterField(
            model_name='trek',
            name='route',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='treks', to='trekking.Route', verbose_name='Route'),
        ),
        migrations.AlterField(
            model_name='trek',
            name='source',
            field=models.ManyToManyField(blank=True, related_name='treks', to='common.RecordSource', verbose_name='Source'),
        ),
        migrations.AlterField(
            model_name='trek',
            name='structure',
            field=models.ForeignKey(default=geotrek.authent.models.default_structure_pk, on_delete=django.db.models.deletion.CASCADE, to='authent.Structure', verbose_name='Related structure'),
        ),
        migrations.AlterField(
            model_name='trek',
            name='themes',
            field=models.ManyToManyField(blank=True, help_text='Main theme(s)', related_name='treks', to='common.Theme', verbose_name='Themes'),
        ),
        migrations.AlterField(
            model_name='trek',
            name='topo_object',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.Topology'),
        ),
        migrations.AlterField(
            model_name='trek',
            name='web_links',
            field=models.ManyToManyField(blank=True, help_text='External resources', related_name='treks', to='trekking.WebLink', verbose_name='Web links'),
        ),
        migrations.AlterField(
            model_name='treknetwork',
            name='network',
            field=models.CharField(max_length=128, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='trekrelationship',
            name='has_common_departure',
            field=models.BooleanField(default=False, verbose_name='Common departure'),
        ),
        migrations.AlterField(
            model_name='trekrelationship',
            name='has_common_edge',
            field=models.BooleanField(default=False, verbose_name='Common edge'),
        ),
        migrations.AlterField(
            model_name='trekrelationship',
            name='is_circuit_step',
            field=models.BooleanField(default=False, verbose_name='Circuit step'),
        ),
        migrations.AlterField(
            model_name='trekrelationship',
            name='trek_a',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trek_relationship_a', to='trekking.Trek'),
        ),
        migrations.AlterField(
            model_name='trekrelationship',
            name='trek_b',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trek_relationship_b', to='trekking.Trek', verbose_name='Trek'),
        ),
        migrations.AlterField(
            model_name='weblink',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='links', to='trekking.WebLinkCategory', verbose_name='Category'),
        ),
        migrations.AlterField(
            model_name='weblink',
            name='name',
            field=models.CharField(max_length=128, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='weblink',
            name='url',
            field=models.URLField(max_length=2048, verbose_name='URL'),
        ),
        migrations.AlterField(
            model_name='weblinkcategory',
            name='label',
            field=models.CharField(max_length=128, verbose_name='Label'),
        ),
        migrations.AlterModelTable(
            name='accessibility',
            table=None,
        ),
        migrations.AlterModelTable(
            name='difficultylevel',
            table=None,
        ),
        migrations.AlterModelTable(
            name='orderedtrekchild',
            table=None,
        ),
        migrations.AlterModelTable(
            name='poi',
            table=None,
        ),
        migrations.AlterModelTable(
            name='poitype',
            table=None,
        ),
        migrations.AlterModelTable(
            name='practice',
            table=None,
        ),
        migrations.AlterModelTable(
            name='route',
            table=None,
        ),
        migrations.AlterModelTable(
            name='service',
            table=None,
        ),
        migrations.AlterModelTable(
            name='servicetype',
            table=None,
        ),
        migrations.AlterModelTable(
            name='trek',
            table=None,
        ),
        migrations.AlterModelTable(
            name='treknetwork',
            table=None,
        ),
        migrations.AlterModelTable(
            name='trekrelationship',
            table=None,
        ),
        migrations.AlterModelTable(
            name='weblink',
            table=None,
        ),
        migrations.AlterModelTable(
            name='weblinkcategory',
            table=None,
        ),
    ]