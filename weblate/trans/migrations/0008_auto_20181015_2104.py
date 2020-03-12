# Generated by Django 1.11.9 on 2018-10-15 19:04

from django.db import migrations

import weblate.trans.fields


class Migration(migrations.Migration):

    dependencies = [("trans", "0007_auto_20181011_1634")]

    operations = [
        migrations.AlterField(
            model_name="component",
            name="language_regex",
            field=weblate.trans.fields.RegexField(
                default="^[^.]+$",
                help_text="Regular expression used to filter translation when scanning for filemask.",
                max_length=500,
                verbose_name="Language filter",
            ),
        )
    ]
