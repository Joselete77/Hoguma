# Generated by Django 4.1.5 on 2023-02-07 01:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_promotion_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='promotion',
            options={'ordering': ['name']},
        ),
    ]