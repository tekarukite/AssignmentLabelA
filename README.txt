# LABEL A - BACKEND ASSIGNMENT - ONLINE CAR PARTS SELLING WEB

TASK INFO (ORIGINAL): https://github.com/LabelA/labela_backend_assignment/blob/main/README.md

GENERAL INFORMATION
-------------------
- This project is made with Django.
- This is only the Backend of the project, so we don't have templates. To test the functionalities, we can use POSTMAN
- We have a table with all the products and one with all the customers. We can register and login with each customer. The products for now are created in the bbdd directly or through the admin Django section.
- Each client has always a Shopping Cart associated (with or without products depending on if the client has chosen some or not).
- When the client chooses a product, it creates a model in the ShoppingCartProducts class that references the product and the amount (we will assume that each time a client chooses a product it increases in 1 the counter of the amount value).
- After choosing all the products, the client can order them to the wanted destination. In that case, we block the shopping Cart (because the client has decided to buy the products) and a new Shopping Cart is created with 0 products in case the client wants to do another shop.
- After the order is created, the client can choose the Delivery day and time to get the products.

HOW TO INSTANCIATE THE PROJECT
------------------------------
1. Download the code (and the bbdd) from the GitHub repository (the bbdd is to test it in local).
2. Create a server and bulk the information ("bbdd_labela") in that server. If there is a problem, create a new database and link it through DATABASES in the "settings.py" file. In this last case, execute later, in step 5, the migration commands of Django.
3. Open a terminal and go to the project folder.
4. Activate the virtual environment (do ".\venv\project-name\Scripts\Activate.ps1" if windows and "source venv/project-name/Scripts/activate" if linux).
5. Activate the server with django ("python manage.py runserver").

If there is an error related with "rest_framework", execute (with the virtual environment activated):
	pip install djangoframework-jsonapi


FUNCTIONALITIES:
---------------
- Register new client: http://localhost:8000/register 

- Acces to the admin section (use secret):
    (Create user and password from the terminal if the database is new)
    User and password: https://onetimesecret.com/secret/j48fgrc67auzor44wcijs96wi455lm2

- Add product to Shopping Cart: 
    URL: http://localhost:8000/web/addToShopCart
    AUTHENTICATION NEEDED
    BODY (form-data): {'product_id': ...}

- Remove product From Shopping Cart: 
    URL: http://localhost:8000/web/removeFromShoppingCart
    AUTHENTICATION NEEDED
    BODY (form-data): {'product_id': ...}

- Order the products: 
    URL: http://localhost:8000/web/newOrder
    AUTHENTICATION NEEDED
    BODY (form-data): {'postal_code': ... , 'city': ... , 'street': ... , 'number': ... , 'more_info': ... }

- Select Delivery Date and time
    URL: http://localhost:8000/web/shopCart/<int:order_id>/selectDeliveryDate
    AUTHENTICATION NEEDED
    BODY (form-data): {'day': ... , 'hour': ... }

- See all product in the Web:
    URL: http://localhost:8000/web/product/all
    AUTHENTICATION NOT NEEDED

- See info about a product:
    URL: http://localhost:8000/web/product/<int:product_id>
    AUTHENTICATION NOT NEEDED
