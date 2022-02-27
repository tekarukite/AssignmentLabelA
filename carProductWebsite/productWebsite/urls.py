from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('product/all', views.showAllWebProductsController),
    path('product/<int:product_id>', views.showProductController),
    path('addToShopCart', views.addToShoppingCartController),
    path('removeFromShoppingCart', views.removeProductFromShoppingCartController),
    path('newOrder', views.newOrderClientController),
    path('shopCart/<int:order_id>/selectDeliveryDate', views.saveDeliveryTimeController),
]