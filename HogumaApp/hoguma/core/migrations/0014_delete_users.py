# Generated by Django 4.1.5 on 2023-02-06 13:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_delete_profile'),
    ]

    operations = [
        migrations.DeleteModel(
            name='users',
        ),
    ]
