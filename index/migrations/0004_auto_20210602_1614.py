# Generated by Django 3.2.3 on 2021-06-02 11:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0003_alter_permissions_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='achievement',
            options={},
        ),
        migrations.AlterModelOptions(
            name='permissions',
            options={'permissions': (('student', 'student'), ('mentor', 'mentor'), ('parvareshi_mentor', 'parvareshi_mentor'), ('amoozeshi_mentor', 'amoozeshi_mentor'), ('pazhooheshi_mentor', 'pazhooheshi_mentor'), ('varzeshi_mentor', 'varzeshi_mentor'), ('manager', 'manager'))},
        ),
    ]
