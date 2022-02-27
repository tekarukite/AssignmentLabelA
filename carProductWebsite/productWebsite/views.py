from django.shortcuts import render
from django.http import HttpResponse
from users.models import CustomUser
from .models import ShoppingCart, Product, ClientOrder, ShoppingCartProducts
from .serializers import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required


def index(request):
    return HttpResponse("Hello, world. You're at the index page.")


def getProduct(product_id):
    try:
        product = Product.objects.get(id=product_id)
    except:
        raise NotFound('Product not found')

    return product


def getUserByEmail(user_email):
    try:
        user = CustomUser.objects.get(email=user_email)
    except:
        raise NotFound('User not found')
    
    return user


def getLastShopCartUser(user_email):
    """
        Gets the Current Shopping Cart of the user. 
        There is only 1 Shopping Cart for user until order done, in which that case the field "order_done" transforms into True and we create a new Shopping Cart with 0 products.
    """
    clientUser = getUserByEmail(user_email)
    last_shop_cart = ShoppingCart.objects.filter(clientUser__id=clientUser.id).filter(order_done=False)

    # The user must always have 1 shopping Cart. If it has more than one, there has been a problem. If it has 0, we create one.
    if len(last_shop_cart) > 1:
        raise NotFound('There is a problem, because we have 2 current shopping Carts for the user')
    
    if len(last_shop_cart) == 0:
        last_shop_cart = ShoppingCart.objects.create(clientUser=clientUser)
        last_shop_cart.save()
        return last_shop_cart


    return last_shop_cart.first()


def computeTotalImport(shop_cart):
    """
        Computes the total import of the Sale
    """
    total = 0
    for shop_product in shop_cart.shop_cart_products.all():
        total = total + shop_product.amount * shop_product.product.price

    return total


# We assume that you only can add 1 unit of the product (if can be more at the same time, we can add a new parameter easily here in phase 2)
def updateShoppingCart(shop_cart, product_id, param):
    """
        param: 'add' or 'remove' (add or remove one value of the amount to the product of the Shopping Cart).
        If the amount is 0, we delete the product from the Shopping Cart
    """
    shop_cart_products = shop_cart.shop_cart_products.all()
    product = Product.objects.filter(id=product_id).first()

    # For each product in the shopping cart we add/substract 1 amount of that product if it exists (if it does not, it doesn't do anything). When the amount reaches 0, we delete that product of the Shopping Cart (instead of having a product with 0 amount)
    found = False
    if len(shop_cart_products) > 0:
        for shop_product in shop_cart_products:
            if shop_product.product.id == product_id:

                if param == 'add':
                    new_amount = shop_product.amount + 1
                    product.remaining_stock = product.remaining_stock - 1
                elif param == 'remove':
                    new_amount = shop_product.amount - 1
                    product.remaining_stock = product.remaining_stock + 1

                shop_product.amount = new_amount
                shop_product.save()
                found = True

                if new_amount == 0:
                    shop_product.delete()

    # It it is a new product, we add it to the Shopping Cart
    if not found and param == 'add':
        product = getProduct(product_id)
        new_product_cart = ShoppingCartProducts.objects.create(product = product)
        shop_cart.shop_cart_products.add(new_product_cart)
        shop_cart.save()

    shop_cart.save()
    product.save()


def addToShoppingCart(shop_cart, product_id):
    updateShoppingCart(shop_cart, product_id, 'add')


def removeFromShoppingCart(shop_cart, product_id):
    updateShoppingCart(shop_cart, product_id, 'remove')


 # In phase 2 we could add an optional parameter that is the amount (in case they can choose amount of that product)
def addProductToShoppingCart(user_email, product_id):
    """
        Adds the product chosen to the ShoppingCart.
    """
    shop_cart = getLastShopCartUser(user_email)
    addToShoppingCart(shop_cart, product_id)
    return shop_cart


def removeProductFromShoppingCart(user_email, product_id):
    """
        Removes the product chosen from the ShoppingCart.
    """
    shop_cart = getLastShopCartUser(user_email)
    removeFromShoppingCart(shop_cart, product_id)
    return shop_cart


# We assume that we can't have more than 1 Order for shopping Cart (when an order is done, a new shopping cart is created).
def newOrderClient(user_email, postal_code, city, street, number, more_info):
    """
        Creates a new Order with the direction to send the products.
    """
    user = getUserByEmail(user_email)
    shop_cart = getLastShopCartUser(user_email)

    if len(shop_cart.shop_cart_products.all()) == 0:
        error = {'message': "There are not products in this Shopping Cart."}
        return error, 400
    
    new_order = ClientOrder.objects.filter(shopCart=shop_cart)

    if len(new_order) == 0:
        total_price = computeTotalImport(shop_cart)
        new_order = ClientOrder.objects.create(shopCart=shop_cart, postal_code=postal_code, city=city, street=street, number=number,    direction_aux=more_info, total_price=total_price)
        new_order.save()

    else:
        error = {'message': "You have already order this Shopping Cart."}
        return error, 400

    # Now that we have ordered, we have to create a new Shopping Cart and block the previous one ordered.
    shop_cart.order_done = True
    shop_cart.save()

    sc = ShoppingCart.objects.create(clientUser=user)
    sc.save()

    return new_order, 200


def saveDeliveryTime(order_id, day, hour):
    """
        Saves into the Order the delivery Date and Time
    """
    try:
        client_order = ClientOrder.objects.get(id=order_id)
    except:
        raise NotFound('Order not found')

    client_order.delivery_date = day
    client_order.delivery_time = hour
    client_order.save()

    return client_order


########################################################
#                    CONTROLLERS                       #
########################################################

@api_view(['POST'])
@login_required()
def addToShoppingCartController(request):
    if request.method == 'POST':
        user_email = request.user.email
        product_id = int(request.POST.get('product_id'))

        # 1. We check that the product_id is a valid one
        product = Product.objects.filter(id=product_id).first()
        if not product:
            raise NotFound('There is no product with this ID')

        # 2. If we don't have enough stock, we can't buy the product.
        if product.remaining_stock < 1:
            error = {'message': "There is no stock available for this product"}
            return Response(data=error, status=400)

        # 3. We add the product to the Shopping Cart
        shop_cart = addProductToShoppingCart(user_email, product_id)
        return Response(ShoppingCartSerializer(shop_cart).data)


@api_view(['POST'])
@login_required()
def removeProductFromShoppingCartController(request):
    if request.method == 'POST':
        user_email = request.user.email
        product_id = int(request.POST.get('product_id'))

        # We check that the product_id is a valid one
        product = Product.objects.filter(id=product_id).first()
        if not product:
            raise NotFound('There is no product with this ID')
        
        shop_cart = removeProductFromShoppingCart(user_email, product_id)
        return Response(ShoppingCartSerializer(shop_cart).data)


@api_view(['GET'])
def showProductController(request, product_id):
    if request.method == 'GET':
        product = getProduct(int(product_id))
        return Response(ProductSerializer(product).data)


@api_view(['GET'])
def showAllWebProductsController(request):
    if request.method == 'GET':
        products = Product.objects.all()
        return Response(ProductSerializer(products, many=True).data)


@login_required()
@api_view(['GET'])
def showProductsShoppingCartController(request, user_email):
    if request.method == 'GET':
        shop_cart = getLastShopCartUser(user_email)
        products = shop_cart.shop_cart_products
        return Response(ProductSerializer(products, many=True).data)


@api_view(['PUT'])
@login_required()
def saveDeliveryTimeController(request, order_id):
    if request.method == 'PUT':
        order_id = int(order_id)

        # We check that the order is from the client:
        try:
            order = ClientOrder.objects.get(id=order_id)
        except:
            raise NotFound('Order not found')

        if order.shopCart.clientUser.email != request.user.email:
            error = {"message": "This client can not update this Order because it is from another customer"}
            return Response(data=error, status=400)


        day = request.POST.get('day')
        hour = request.POST.get('hour')
        client_order = saveDeliveryTime(order_id, day, hour)
        return Response(OrderSerializer(client_order).data)


@api_view(['POST'])
@login_required()
def newOrderClientController(request):
    if request.method == 'POST':

        user_email = request.user.email
        postal_code = request.POST.get('postal_code')
        city = request.POST.get('city')
        street = request.POST.get('street')
        number = request.POST.get('number')
        more_info = request.POST.get('more_info')

        result, code = newOrderClient(user_email, postal_code, city, street, number, more_info)
        if code == 200:
            return Response(OrderSerializer(result).data)
        else:
            return Response(data=result, status=400)
