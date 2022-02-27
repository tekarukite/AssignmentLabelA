# Generated by Django 3.1 on 2022-02-26 21:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('productWebsite', '0007_auto_20220226_0051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.FloatField(default=0.0, verbose_name='Price'),
        ),
        migrations.CreateModel(
            name='ShoppingCartProducts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=0, verbose_name='Amount')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='productWebsite.product')),
            ],
        ),
        migrations.AlterField(
            model_name='shoppingcart',
            name='products',
            field=models.ManyToManyField(to='productWebsite.ShoppingCartProducts'),
        ),
    ]
