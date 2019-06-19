from __future__ import absolute_import, print_function

from decimal import Decimal
from datetime import datetime

from pony.orm import *
from os.path import expanduser
from os import makedirs

db_path = expanduser("~") + "/.local/share/sshorganizer"
makedirs(db_path, exist_ok=True)
db_file = db_path + "/organizer.sqlite"

db = Database("sqlite", db_file, create_db=True)

class Customer(db.Entity):
    email = Required(str, unique=True)
    password = Required(str)
    name = Required(str)
    country = Required(str)
    address = Required(str)
    cart_items = Set("CartItem")
    orders = Set("Order")

class Product(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    categories = Set("Category")
    description = Optional(str)
    picture = Optional(buffer)
    price = Required(Decimal)
    quantity = Required(int)
    cart_items = Set("CartItem")
    order_items = Set("OrderItem")

class CartItem(db.Entity):
    quantity = Required(int)
    customer = Required(Customer)
    product = Required(Product)

class OrderItem(db.Entity):
    quantity = Required(int)
    price = Required(Decimal)
    order = Required("Order")
    product = Required(Product)
    PrimaryKey(order, product)

class Order(db.Entity):
    id = PrimaryKey(int, auto=True)
    state = Required(str)
    date_created = Required(datetime)
    date_shipped = Optional(datetime)
    date_delivered = Optional(datetime)
    total_price = Required(Decimal)
    customer = Required(Customer)
    items = Set(OrderItem)

class Category(db.Entity):
    name = Required(str, unique=True)
    products = Set(Product)

sql_debug(False)

db.generate_mapping(create_tables=True)
