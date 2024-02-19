# Emte Ecommerce API

Emte Ecommerce API provides infrastructure for Product, Basket, and Order processes, supporting various operations within the system.

## How to Run
### Docker and Docker Compose
The easiest way to build and run the project is using Docker with docker-compose.

Build and run the project with the following terminal command:
docker-compose up --build

Alternatively, you can set up a virtual environment and install the required packages from `requirements.txt`.

Migrate the migrations to the SQLite database using the command:
python manage.py migrate --settings=app.sqlite

Run the server with the command:
python manage.py runserver 0.0.0.0:8000 --settings=app.sqlite

Create an admin account using the command:
python manage.py createsuperuser --settings=app.sqlite

## System Architecture

### Product
A product is the central element of the system, created by sellers with attributes such as name, category, images, features, and variants, each with a description and price.

Buyers add products to their baskets, which are stored as receipts containing product details and additional information.

After a purchase, products are kept in an order object for future reference.

#### Product Variants
A product variant is a version of a product with minor differences. Each variant has its own name, description, and price.

When a product's variant changes, the information of the previous variant remains hidden in the market, preserving purchase details and tracking seller activity.

#### Product Features
Products can be described in more detail by specifying their features. The features and their values are determined by the admin.

A product inherits features from its category and the category's parents. The list of allowed features is a cumulative sum of the features up the hierarchy, without blocking the parent's features.

#### Product Images
A product can have multiple images.

### Receipt
A receipt contains information about a product variant, basket count, and date. It retains information even after the product variant's features change.

All receipts are initially linked to an order object with a null purchase date.

Before a purchase, they represent products in the basket.

After a purchase, they serve as a record of the transaction.

### Order
An order object aggregates all information related to a purchase, including the products, variants, and receipts.

### User
Users can be both buyers and sellers in the system.

Registration requires an email address, password, and basic personal information.

## Security

### Django Rest Framework
The API and system are built on the Django Rest Framework, a trusted and widely-used web framework.

### Ownership of Objects
Object ownership is controlled by viewset permissions. Users can only update and delete their own user profiles, products, receipts, and orders.

Receipts and orders can only be updated before the purchase is finalized.

### Preventing Inappropriate Content
Inappropriate content is prevented by requiring admin approval for changes before they are displayed in the system.

## Admin Panel

### Displayed Columns
Critical columns of the models are displayed in the Django Admin Panel for easy management.

### Filters
Critical fields are provided as filters on the model display page for better accessibility. Some related objects' fields are also included as filters.

### Restricted Actions
Due to the complexity of product, receipt, and order operations, they are managed exclusively through views and serializers.
