# Generated by Django 3.2.18 on 2023-04-07 09:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authent', '0011_alter_userprofile_structure'),
        ('common', '0031_auto_20230407_0947'),
        ('land', '0008_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='competenceedge',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='common.organism', verbose_name='Organism'),
        ),
        migrations.AlterField(
            model_name='landedge',
            name='land_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='land.landtype', verbose_name='Land type'),
        ),
        migrations.AlterField(
            model_name='landtype',
            name='structure',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='authent.structure', verbose_name='Related structure'),
        ),
        migrations.AlterField(
            model_name='physicaledge',
            name='physical_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='land.physicaltype', verbose_name='Physical type'),
        ),
        migrations.AlterField(
            model_name='physicaltype',
            name='structure',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='authent.structure', verbose_name='Related structure'),
        ),
        migrations.AlterField(
            model_name='signagemanagementedge',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='common.organism', verbose_name='Organism'),
        ),
        migrations.AlterField(
            model_name='workmanagementedge',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='common.organism', verbose_name='Organism'),
        ),
    ]