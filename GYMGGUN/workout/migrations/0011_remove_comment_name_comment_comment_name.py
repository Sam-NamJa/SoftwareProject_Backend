# Generated by Django 4.0.4 on 2022-05-23 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workout', '0010_comment_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='name',
        ),
        migrations.AddField(
            model_name='comment',
            name='comment_name',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
