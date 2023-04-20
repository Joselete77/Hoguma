# Generated by Django 4.1.5 on 2023-04-20 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0038_restaurantdetails'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotelinformation',
            name='latitude',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='hotelinformation',
            name='longitude',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]