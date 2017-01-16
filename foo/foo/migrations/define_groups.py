from django.contrib.auth.models import Group
from django.db import migrations


def create_groups(apps, schema_editor):
    if not schema_editor.connection.alias == 'default':
        return

    Group.objects.get_or_create(name='fun_users')


class Migration(migrations.Migration):

    dependencies = [
        ('foo', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_groups),
    ]
