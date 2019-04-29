# Generated by Django 2.2 on 2019-04-27 18:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tccStudentRegistration', '0005_auto_20190424_0157'),
    ]

    operations = [
        migrations.AddField(
            model_name='matricula',
            name='curso',
            field=models.ForeignKey(blank=True, help_text='Curso em que a matricula foi feita', null=True, on_delete=django.db.models.deletion.CASCADE, to='tccStudentRegistration.Curso', verbose_name='Curso'),
        ),
    ]
