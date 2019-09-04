# Generated by Django 2.2.4 on 2019-09-04 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Mainevent', '0004_auto_20190904_0956'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('e_id', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('event_name', models.CharField(max_length=50)),
                ('keywords_dict', models.CharField(max_length=100)),
                ('begin_timestamp', models.BigIntegerField()),
                ('begin_date', models.DateField()),
                ('end_timestamp', models.BigIntegerField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('content', models.CharField(max_length=400)),
                ('uid', models.CharField(blank=True, max_length=30, null=True)),
            ],
            options={
                'db_table': 'Event',
            },
        ),
        migrations.CreateModel(
            name='Hot_post',
            fields=[
                ('h_id', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('uid', models.CharField(max_length=30)),
                ('root_uid', models.CharField(max_length=30)),
                ('mid', models.CharField(max_length=30)),
                ('comment', models.IntegerField()),
                ('retweeted', models.IntegerField()),
                ('text', models.CharField(max_length=400)),
                ('keywords_dict', models.CharField(max_length=100)),
                ('timestamp', models.BigIntegerField()),
                ('date', models.DateField()),
                ('ip', models.CharField(max_length=20)),
                ('geo', models.CharField(max_length=50)),
                ('message_type', models.IntegerField()),
                ('root_mid', models.CharField(max_length=30)),
                ('source', models.CharField(max_length=20)),
                ('store_timestamp', models.BigIntegerField()),
                ('store_date', models.DateField()),
            ],
            options={
                'db_table': 'Hot_post',
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('t_id', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('task_type', models.IntegerField()),
                ('into_type', models.IntegerField()),
                ('status', models.IntegerField()),
                ('uid', models.CharField(blank=True, max_length=30, null=True)),
                ('root_uid', models.CharField(blank=True, max_length=30, null=True)),
                ('mid', models.CharField(blank=True, max_length=30, null=True)),
                ('comment', models.IntegerField(blank=True, null=True)),
                ('retweeted', models.IntegerField(blank=True, null=True)),
                ('text', models.CharField(max_length=400)),
                ('keywords_dict', models.CharField(max_length=100)),
                ('timestamp', models.BigIntegerField(blank=True, null=True)),
                ('date', models.DateField(blank=True, null=True)),
                ('ip', models.CharField(blank=True, max_length=20, null=True)),
                ('geo', models.CharField(blank=True, max_length=50, null=True)),
                ('message_type', models.IntegerField(blank=True, null=True)),
                ('root_mid', models.CharField(blank=True, max_length=30, null=True)),
                ('source', models.CharField(max_length=20)),
                ('into_timestamp', models.BigIntegerField()),
                ('into_date', models.DateField()),
            ],
            options={
                'db_table': 'Task',
            },
        ),
        migrations.CreateModel(
            name='Information',
            fields=[
                ('i_id', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('uid', models.CharField(max_length=30)),
                ('root_uid', models.CharField(max_length=30)),
                ('mid', models.CharField(max_length=30)),
                ('comment', models.IntegerField()),
                ('retweeted', models.IntegerField()),
                ('text', models.CharField(max_length=400)),
                ('keywords_dict', models.CharField(max_length=100)),
                ('timestamp', models.BigIntegerField()),
                ('date', models.DateField()),
                ('ip', models.CharField(max_length=20)),
                ('geo', models.CharField(max_length=50)),
                ('message_type', models.IntegerField()),
                ('root_mid', models.CharField(max_length=30)),
                ('source', models.CharField(max_length=20)),
                ('i_level', models.IntegerField()),
                ('event', models.ManyToManyField(to='Mainevent.Event')),
            ],
            options={
                'db_table': 'Information',
            },
        ),
        migrations.CreateModel(
            name='Figure',
            fields=[
                ('f_id', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('gender', models.NullBooleanField()),
                ('follow_num', models.IntegerField(blank=True, null=True)),
                ('fans_num', models.IntegerField(blank=True, null=True)),
                ('tweets_num', models.IntegerField(blank=True, null=True)),
                ('authentication', models.CharField(blank=True, max_length=50, null=True)),
                ('address', models.CharField(blank=True, max_length=50, null=True)),
                ('event', models.ManyToManyField(to='Mainevent.Event')),
            ],
            options={
                'db_table': 'Figure',
            },
        ),
    ]
