# Generated by Django 4.0.4 on 2022-05-11 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_alter_accountlist_table_alter_usersinfo_table'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='accountlist',
            name='id',
        ),
        migrations.AlterField(
            model_name='accountlist',
            name='UID',
            field=models.CharField(max_length=100, primary_key=True, serialize=False, unique=True),
        ),
    ]
