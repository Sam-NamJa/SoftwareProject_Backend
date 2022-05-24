# Generated by Django 4.0.4 on 2022-05-24 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0004_alter_portfolios_contentimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('image', models.FileField(null=True, upload_to='contentImage/')),
            ],
        ),
    ]