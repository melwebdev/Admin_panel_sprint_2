# Generated by Django 3.1 on 2021-06-22 18:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('movies', '0002_add_index_on_person_name'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='personrole',
            name='movies_pers_filmwor_91be89_idx',
        ),
        migrations.AddIndex(
            model_name='personrole',
            index=models.Index(fields=['filmwork'], name='movies_pers_filmwor_deddf5_idx'),
        ),
        migrations.AddIndex(
            model_name='personrole',
            index=models.Index(fields=['person'], name='movies_pers_person__789609_idx'),
        ),
    ]
