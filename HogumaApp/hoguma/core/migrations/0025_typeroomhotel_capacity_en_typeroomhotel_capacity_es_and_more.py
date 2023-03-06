# Generated by Django 4.1.5 on 2023-03-04 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_alter_refund_makerefund'),
    ]

    operations = [
        migrations.AddField(
            model_name='typeroomhotel',
            name='capacity_en',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='typeroomhotel',
            name='capacity_es',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='typeroomhotel',
            name='description_en',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='typeroomhotel',
            name='description_es',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='typeroomhotel',
            name='name_en',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='typeroomhotel',
            name='name_es',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='typeroomhotel',
            name='price_en',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='typeroomhotel',
            name='price_es',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='typeroomhotel',
            name='roomAvailable_en',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='typeroomhotel',
            name='roomAvailable_es',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='typeroomhotel',
            name='type_en',
            field=models.CharField(default=0, max_length=50, null=True, verbose_name='Type room'),
        ),
        migrations.AddField(
            model_name='typeroomhotel',
            name='type_es',
            field=models.CharField(default=0, max_length=50, null=True, verbose_name='Type room'),
        ),
    ]
