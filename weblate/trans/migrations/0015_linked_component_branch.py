# Generated by Django 1.11.18 on 2019-02-12 19:47

from django.db import migrations


def update_linked(apps, schema_editor):
    """Clean branch for linked components."""
    Component = apps.get_model("trans", "Component")
    db_alias = schema_editor.connection.alias
    linked = Component.objects.using(db_alias).filter(repo__startswith="weblate:")
    linked.update(branch="")


class Migration(migrations.Migration):

    dependencies = [("trans", "0014_auto_20190203_1923")]

    operations = [
        migrations.RunPython(update_linked, reverse_code=update_linked, elidable=True)
    ]
