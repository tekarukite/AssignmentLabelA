from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.conf import settings


class Product(models.Model):
    name = models.CharField(max_length=80, blank=True, null=True)
    reference = models.CharField(max_length=20, blank=True, null=True)
    description = models.TextField(max_length=500, blank=True, null=True)
    remaining_stock = models.IntegerField(default=0)
    price = models.FloatField(verbose_name='Price', default=0.00)
    # In phase 2 we could put more info in this product class: car brand (model), image of the product, type of the product, ...

    class Meta:
        ordering = ['reference']

    def __str__(self):
        return "%s %s" % (self.name, self.reference)

# In this class we put the info chosen for the product (amount, colours, model, ...)
class ShoppingCartProducts(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.IntegerField(verbose_name='Amount', default=1)


class ShoppingCart(models.Model):
    shop_cart_products = models.ManyToManyField(ShoppingCartProducts)
    clientUser = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order_done = models.BooleanField(default=False)

    class Meta:
        ordering = ['id']


# Order
class ClientOrder(models.Model):
    shopCart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)

    postal_code = models.CharField(verbose_name='PostalCode', max_length=20)
    city = models.CharField(verbose_name='City', max_length=100)
    street = models.CharField(verbose_name='Name Street', max_length=100)
    number = models.CharField(verbose_name='Number', max_length=10)
    direction_aux = models.TextField(verbose_name='More info of the Direction', blank=True, null=True, max_length=200)
    total_price = models.FloatField(verbose_name="Total Import", default=0.00)

    delivery_date = models.DateField(verbose_name='Delivery Date', blank=True, null=True)
    delivery_time = models.TimeField(verbose_name='Delivery Hour', blank=True, null=True)

    class Meta:
        ordering = ['id']