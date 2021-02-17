# Generated by Django 1.11.11 on 2018-06-08 10:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('maintenance', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contractor',
            name='structure',
            field=models.ForeignKey(blank=True, db_column='structure', default=settings.DEFAULT_STRUCTURE_PK, null=True, on_delete=django.db.models.deletion.CASCADE, to='authent.Structure', verbose_name='Related structure'),
        ),
        migrations.AlterField(
            model_name='intervention',
            name='length',
            field=models.FloatField(blank=True, db_column='longueur', default=0.0, null=True, verbose_name='3D Length'),
        ),
        migrations.AlterField(
            model_name='interventiondisorder',
            name='structure',
            field=models.ForeignKey(blank=True, db_column='structure', default=settings.DEFAULT_STRUCTURE_PK, null=True, on_delete=django.db.models.deletion.CASCADE, to='authent.Structure', verbose_name='Related structure'),
        ),
        migrations.AlterField(
            model_name='interventionjob',
            name='structure',
            field=models.ForeignKey(blank=True, db_column='structure', default=settings.DEFAULT_STRUCTURE_PK, null=True, on_delete=django.db.models.deletion.CASCADE, to='authent.Structure', verbose_name='Related structure'),
        ),
        migrations.AlterField(
            model_name='interventionstatus',
            name='structure',
            field=models.ForeignKey(blank=True, db_column='structure', default=settings.DEFAULT_STRUCTURE_PK, null=True, on_delete=django.db.models.deletion.CASCADE, to='authent.Structure', verbose_name='Related structure'),
        ),
        migrations.AlterField(
            model_name='interventiontype',
            name='structure',
            field=models.ForeignKey(blank=True, db_column='structure', default=settings.DEFAULT_STRUCTURE_PK, null=True, on_delete=django.db.models.deletion.CASCADE, to='authent.Structure', verbose_name='Related structure'),
        ),
        migrations.AlterField(
            model_name='projectdomain',
            name='structure',
            field=models.ForeignKey(blank=True, db_column='structure', default=settings.DEFAULT_STRUCTURE_PK, null=True, on_delete=django.db.models.deletion.CASCADE, to='authent.Structure', verbose_name='Related structure'),
        ),
        migrations.AlterField(
            model_name='projecttype',
            name='structure',
            field=models.ForeignKey(blank=True, db_column='structure', default=settings.DEFAULT_STRUCTURE_PK, null=True, on_delete=django.db.models.deletion.CASCADE, to='authent.Structure', verbose_name='Related structure'),
        ),
    ]
