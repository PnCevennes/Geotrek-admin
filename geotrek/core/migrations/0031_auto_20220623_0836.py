# Generated by Django 3.1.14 on 2022-06-23 08:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authent', '0009_userprofile_extended_username'),
        ('core', '0030_auto_20220127_0939'),
    ]

    operations = [
        migrations.CreateModel(
            name='CertificationLabel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=128, verbose_name='Name')),
                ('structure', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='authent.structure', verbose_name='Related structure')),
            ],
            options={
                'verbose_name': 'Related structures',
                'verbose_name_plural': 'Related structure',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CertificationStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=128, verbose_name='Name')),
                ('structure', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='authent.structure', verbose_name='Related structure')),
            ],
            options={
                'verbose_name': 'Related structures',
                'verbose_name_plural': 'Related structure',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CertificationTrail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('certification_label', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='certifications', to='core.certificationlabel', verbose_name='Certification label')),
                ('certification_status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='certifications', to='core.certificationstatus', verbose_name='Certification status')),
                ('structure', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='authent.structure', verbose_name='Related structure')),
            ],
            options={
                'verbose_name': 'Related structures',
                'verbose_name_plural': 'Related structure',
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='trail',
            name='certifications',
            field=models.ManyToManyField(blank=True, related_name='trails', to='core.CertificationTrail', verbose_name='Certifications'),
        ),
    ]
