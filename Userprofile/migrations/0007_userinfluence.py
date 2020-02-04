# Generated by Django 2.2.4 on 2020-01-17 04:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Userprofile', '0006_merge_20200117_0429'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfluence',
            fields=[
                ('uid', models.CharField(blank=True, max_length=30, primary_key=True, serialize=False)),
                ('timestamp', models.BigIntegerField(blank=True, null=True)),
                ('influence', models.IntegerField(blank=True, null=True)),
                ('importance', models.IntegerField(blank=True, null=True)),
                ('activity', models.IntegerField(blank=True, null=True)),
                ('sensitity', models.IntegerField(blank=True, null=True)),
                ('store_date', models.DateField(blank=True, null=True)),
            ],
            options={
                'db_table': 'UserInfluence',
            },
        ),
    ]