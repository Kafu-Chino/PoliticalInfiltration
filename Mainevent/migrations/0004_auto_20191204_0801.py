# Generated by Django 2.2.4 on 2019-12-04 08:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Mainevent', '0003_auto_20191203_0754'),
    ]

    operations = [
        migrations.RenameField(
            model_name='figure',
            old_name='domian',
            new_name='domain',
        ),
    ]