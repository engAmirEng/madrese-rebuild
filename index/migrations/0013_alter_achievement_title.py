# Generated by Django 3.2.3 on 2021-06-08 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0012_alter_achievement_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='achievement',
            name='title',
            field=models.CharField(max_length=50),
        ),
    ]
