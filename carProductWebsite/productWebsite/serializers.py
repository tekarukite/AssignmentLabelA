from rest_framework import serializers
from . import models


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = ('__all__')


class ShoppingCartProductsSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    
    class Meta:
        model = models.ShoppingCartProducts
        fields = ('__all__')


class ShoppingCartSerializer(serializers.ModelSerializer):
    shop_cart_products = ShoppingCartProductsSerializer(read_only=True, many=True)

    class Meta:
        model = models.ShoppingCart
        fields = ('__all__')


class OrderSerializer(serializers.ModelSerializer):
    shopCart = ShoppingCartSerializer(read_only=True)
    
    class Meta:
        model = models.ClientOrder
        fields = ('__all__')