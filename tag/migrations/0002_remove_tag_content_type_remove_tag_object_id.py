# Generated by Django 4.0.5 on 2022-09-16 16:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tag', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='tag',
            name='object_id',
        ),
    ]
