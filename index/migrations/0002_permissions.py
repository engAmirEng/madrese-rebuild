# Generated by Django 3.2.3 on 2021-06-02 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Permissions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'permissions': (('student', 'student'), ('amoozeshi_mentor', 'amoozeshi_mentor'), ('pazhooheshi_mentor', 'pazhooheshi_mentor'), ('varzeshi_mentor', 'varzeshi_mentor'), ('manager', 'manager')),
            },
        ),
    ]