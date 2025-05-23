# Generated by Django 5.1.3 on 2025-03-15 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0004_postcategory_postcategoryevent_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="tags",
            field=models.ManyToManyField(
                blank=True,
                related_name="posts",
                through="core.PostObjectTag",
                to="core.posttag",
            ),
        ),
    ]
