from sqlalchemy.sql import text
from db import db
from datetime import datetime
import menu

def create_order(user_id, restaurant_id, total_price):
    create_order_query = ("INSERT INTO Orders (user_id, restaurant_id, total_price, logged_at, delivered) VALUES (:user_id, :restaurant_id, :total_price, :logged_at, :delivered) RETURNING id")
    order_id = db.session.execute(text(create_order_query), {"user_id": user_id, "restaurant_id": restaurant_id, "total_price": total_price, "logged_at": datetime.now(), "delivered":False}).fetchone()[0]
    db.session.commit()
    return order_id

#ordered_items is a list of tuples, where the first value is an ordered item and the second value is the amount
def add_order_items(order_id, ordered_items):
    order_item_add_query = ("INSERT INTO OrderItems (order_id, menuItem_id, item_name, quantity, price) VALUES (:order_id, :menuItem_id, :item_name, :quantity, :price)")
    for item in ordered_items:
        print(item)
        db.session.execute(text(order_item_add_query), {"order_id": order_id, "menuItem_id": item[0].id, "item_name":item[0].item_name, "quantity":item[1], "price":item[0].price})
        db.session.commit()

def get_orders_for_user(user_id):
    sql = ("""SELECT o.id, o.logged_at, r.name
    FROM orders o
    JOIN restaurants r ON o.restaurant_id = r.id
    WHERE o.user_id = :user_id;""")
    orders = db.session.execute(text(sql), {"user_id":user_id}).fetchall()
    for order in orders:
        print(order)
    return orders

def get_orders_for_restaurant(restaurant_id):
    sql = "SELECT * FROM orders WHERE restaurant_id=:restaurant_id"
    orders = db.session.execute(text(sql), {"restaurant_id":restaurant_id}).fetchall()
    for order in orders:
        print(order)
    return orders

def get_restaurant_id_from_order(order_id):
    sql  = "SELECT restaurant_id FROM Orders WHERE id=:order_id"
    restaurant_id = db.session.execute(text(sql), {"order_id":order_id}).fetchone()[0]
    return restaurant_id

def get_order_items(order_id):
    sql = "SELECT * FROM OrderItems WHERE order_id=:order_id"
    ordered_items = db.session.execute(text(sql), {"order_id":order_id}).fetchall()
    return ordered_items

def total_price_of_order(order_id):
    sql = "SELECT total_price FROM Orders WHERE id=:order_id"
    price = db.session.execute(text(sql), {"order_id":order_id}).fetchone()[0]
    return price

def order_owned_by_user(user_id, order_id):
    sql = ("SELECT user_id FROM orders WHERE id=:order_id")
    id = db.session.execute(text(sql), {"order_id":order_id}).fetchone()[0]
    return id == user_id

def get_delivery_status(order_id):
    sql = "SELECT delivered from orders WHERE id=:order_id"
    delivery_status = db.session.execute(text(sql), {"order_id":order_id}).fetchone()[0]
    return delivery_status
