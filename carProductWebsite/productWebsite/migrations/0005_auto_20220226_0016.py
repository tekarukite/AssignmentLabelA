# Generated by Django 3.1 on 2022-02-25 23:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productWebsite', '0004_auto_20220226_0002'),
    ]

    operations = [
        migrations.AddField(
            model_name='shoppingcart',
            name='delivery_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='shoppingcart',
            name='delivery_time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
