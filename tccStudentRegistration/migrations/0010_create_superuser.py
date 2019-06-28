from __future__ import unicode_literals

from django.db import migrations


def create_superuser(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    user_admin = User.objects.filter(username='admin')
    if len(user_admin) > 0:
        user_admin = user_admin[0]
    else:
        user_admin = User.objects.create(is_superuser=True, username='admin',
                                         email='admin@admin.com',
                                         first_name="Admin", last_name="Admin",
                                         is_staff=True, is_active=True,
                                         password='a1b2c3d4',)


def revert(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('tccStudentRegistration', '0009_auto_20190428_1917'),
    ]

    operations = [
        migrations.RunPython(create_superuser, revert)
    ]
