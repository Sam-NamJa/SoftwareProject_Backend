# Generated by Django 4.0.4 on 2022-05-24 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_alter_portfolios_contentimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='portfolios',
            name='contentImage',
            field=models.FileField(null=True, upload_to='contentImage/'),
        ),
    ]
