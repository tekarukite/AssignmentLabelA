# Generated by Django 3.1 on 2022-02-27 00:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productWebsite', '0008_auto_20220226_2256'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shoppingcart',
            old_name='sale_done',
            new_name='order_done',
        ),
        migrations.AddField(
            model_name='clientorder',
            name='total_price',
            field=models.FloatField(default=0.0, verbose_name='Total Import'),
        ),
        migrations.AlterField(
            model_name='shoppingcartproducts',
            name='amount',
            field=models.IntegerField(default=1, verbose_name='Amount'),
        ),
    ]
