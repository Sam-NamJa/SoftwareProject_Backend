# Generated by Django 4.0.4 on 2022-05-11 17:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0005_alter_accountlist_uid_alter_usersinfo_uid'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlanList',
            fields=[
                ('planName', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('like', models.SmallIntegerField(default=0)),
                ('download', models.SmallIntegerField(default=0)),
                ('hashTagChest', models.CharField(max_length=10, null=True)),
                ('hashTagBack', models.CharField(max_length=10, null=True)),
                ('hashTagLeg', models.CharField(max_length=10, null=True)),
                ('hashTagShoulder', models.CharField(max_length=10, null=True)),
                ('hashTagArm', models.CharField(max_length=10, null=True)),
                ('hashTagAir', models.CharField(max_length=10, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('UID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.accountlist')),
            ],
            options={
                'db_table': 'PlanList',
                'ordering': ['updated_at'],
            },
        ),
        migrations.CreateModel(
            name='WorkoutList',
            fields=[
                ('workoutID', models.AutoField(primary_key=True, serialize=False)),
                ('dayCount', models.SmallIntegerField(default=1)),
                ('workoutName', models.CharField(max_length=20)),
                ('set', models.SmallIntegerField(blank=True, null=True)),
                ('times', models.SmallIntegerField(blank=True, null=True)),
                ('weight', models.SmallIntegerField(blank=True, null=True)),
                ('isComplete', models.SmallIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('UID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.accountlist')),
                ('planName', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workout.planlist')),
            ],
            options={
                'db_table': 'WorkoutList',
                'ordering': ['updated_at'],
            },
        ),
    ]
