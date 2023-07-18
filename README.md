# Emte Ecommerce API

Emte Ecommerce API provides an infrastructure for Product, Basket and Order processes to every part of the operation.

## How to run
### Docker and Docker compose
The easiest way to build and run the project is to use Docker with docker-compose.

You can build and up the project by the terminal command
: docker-compose up --build

### Virtual environment
Otherwise you need to build a virtual environment and install the packages on the requirements.txt.

Then migrate the migrations on the sqlite database by the command : python manage.py migrate --settings=app.sqlite

Then you can run the server by the command : python manage.py runserver 0.0.0.0:8000 --settings=app.sqlite

You can create an admin account by the command : python manage.py createsuperuser --settings=app.sqlite

## How to try
You can easily send requests by using postman collection.

Here is the postman collection link, just import the collection and start to try
https://www.getpostman.com/collections/68c103eb1721232ec101

## System Architecture

### Product
A product is the subject of the whole process. It is created by seller with a name, a category, images, features, variants with a description and a price for each.

A buyer adds a product to his/her basket. It is kept as a receipt which represents the basket product with a few extra information.

After purchase is completed, products remain in an order object for future display.

#### Product Variants
A product variant is an altered version with a small difference from the other variants. A variant has a name, description and its own price.

After a product's variant changes, previous variant's information remains as invisible to the market. This rule lets purchase informations remain and is necessary for tracking seller activity.

#### Product Features
A product can be more descriptive by getting specified its features. Features and value of these features of a product are determined by the admin.

A product inherits its features from its category and parents of the category. The list of the allowed features is a sum of the features while parent exists and it does not block its parent's features.

#### Product Images
A product can have multiple images.

### Receipt
A receipt holds product variant, basket count and date information of the products. Information remains even after features of the product variant change.

All receipts are bonded to an order object with a null purchase date at the first step.

Before the purchase, they represent products in the basket.

After the purchase, they become the memory of the order operation.

### Order
An order object keeps together all the information about a purchase, including the objects mentioned above.

### User
A user can become both a buyer and a seller on the system.

It simply requires an email address and a password with some other basic information.

## Security

### Django Rest Framework
API and the system is built on Django Rest Framework. It is already a trusted web framework which is used by millions.

### Ownership of the objects
Ownership of the objects are controlled by viewset permissions. Everyone can update and delete only their own user, products, receipts and orders.

Receipts and orders can be updated only before the purchase.

### Preventing inconvenient content
Inconvenient contents are prevented by the requirement of admin approve for changes before they show up on the system.

## Admin Panel

### Displayed columns
Most necessarry columns of the models are considered and displayed on the Django Admin Panel.

### Filters
Critique fields are considered for better accesibility and provided as filters on the model display page. As critique fields, some of the related objects' fields are also added to the filters.

### Restricted actions
Product, receipt and order operations are quite a bit complicated. So they are handled well only through views and serializers.

Any manuel update on the Django admin panel can cause an unexpected and chain error on the system. So actions on the Django admin panel are restricted for the sake of the operations.

