# Generated by Django 4.0.5 on 2022-09-16 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tag', '0002_remove_tag_content_type_remove_tag_object_id'),
        ('recipes', '0003_alter_recipe_category_alter_recipe_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(to='tag.tag'),
        ),
    ]
