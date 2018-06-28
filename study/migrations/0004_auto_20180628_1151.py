# Generated by Django 2.0.6 on 2018-06-28 03:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('study', '0003_auto_20180627_1036'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entryrecord',
            name='created_at',
        ),
        migrations.AddField(
            model_name='entryrecord',
            name='learned_at',
            field=models.DateTimeField(blank=True, db_index=True, default=None, null=True),
        ),
    ]
