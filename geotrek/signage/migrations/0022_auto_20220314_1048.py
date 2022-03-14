# Generated by Django 3.1.14 on 2022-03-14 10:48

from django.db import migrations
from django.conf import settings


def forward(apps, schema_editor):
    with schema_editor.connection.cursor() as cursor:
        cursor.execute(
            "SELECT 1 FROM information_schema.columns WHERE table_name='signage_signage' AND column_name='published'"
        )
        if cursor.fetchone():
            for lang in settings.MODELTRANSLATION_LANGUAGES:
                cursor.execute(
                    f"SELECT 1 FROM information_schema.columns WHERE table_name='signage_signage' AND column_name='published_{lang}'"
                )
                if not cursor.fetchone():
                    cursor.execute(
                        f"ALTER TABLE signage_signage ADD published_{lang} Boolean DEFAULT FALSE;"
                    )
                    cursor.execute(
                        f"UPDATE signage_signage SET published_{lang} = True WHERE published = True;"
                    )


def backward(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('signage', '0021_auto_20210908_1306'),
    ]

    operations = [
        migrations.RunPython(forward, backward),
    ]
