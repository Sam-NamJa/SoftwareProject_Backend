# Generated by Django 4.0.4 on 2022-05-24 05:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('workout', '0011_remove_comment_name_comment_comment_name'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Comment',
            new_name='PlanComment',
        ),
    ]