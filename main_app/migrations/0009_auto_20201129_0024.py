# Generated by Django 3.1.2 on 2020-11-29 00:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0008_auto_20201125_0454'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='name',
            new_name='title',
        ),
    ]