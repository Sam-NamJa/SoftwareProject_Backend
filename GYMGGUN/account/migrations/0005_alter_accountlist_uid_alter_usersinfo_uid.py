# Generated by Django 4.0.4 on 2022-05-11 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_alter_usersinfo_uid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountlist',
            name='UID',
            field=models.CharField(max_length=100, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='usersinfo',
            name='UID',
            field=models.CharField(max_length=100, primary_key=True, serialize=False),
        ),
    ]