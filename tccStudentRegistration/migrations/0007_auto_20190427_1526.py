# Generated by Django 2.2 on 2019-04-27 18:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tccStudentRegistration', '0006_matricula_curso'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matricula',
            name='curso',
            field=models.ForeignKey(help_text='Curso em que a matricula foi feita', on_delete=django.db.models.deletion.CASCADE, to='tccStudentRegistration.Curso', verbose_name='Curso'),
        ),
    ]