# Generated by Django 4.1.5 on 2023-03-04 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0027_remove_typeroomhotel_description_en_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='promotion',
            name='description_en',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='promotion',
            name='description_es',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='promotion',
            name='name_en',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='promotion',
            name='name_es',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
