from sqlalchemy.sql import text
from db import db
from datetime import datetime

def create_order(user_id, restaurant_id, total_price):
    create_order_query = ("INSERT INTO Orders (user_id, restaurant_id, total_price, logged_at) VALUES (:user_id, :restaurant_id, :total_price, :logged_at) RETURNING id")
    order_id = db.session.execute(text(create_order_query), {"user_id": user_id, "restaurant_id": restaurant_id, "total_price": total_price, "logged_at": datetime.now()}).fetchone()[0]
    db.session.commit()
    return order_id

#ordered_items is a list of tuples, where the first value is an ordered item and the second value is the amount
def add_order_items(order_id, ordered_items):
    order_item_add_query = ("INSERT INTO OrderItems (order_id, menuItem_id, quantity, price) VALUES (:order_id, :menuItem_id, :quantity, :price)")
    for item in ordered_items:
        print(item)
        db.session.execute(text(order_item_add_query), {"order_id": order_id, "menuItem_id": item[0].id, "quantity":item[1], "price":item[0].price})
        db.session.commit()

def get_orders(user_id):
    sql = ("""SELECT o.id, o.logged_at, r.name
    FROM orders o
    JOIN restaurants r ON o.restaurant_id = r.id
    WHERE o.user_id = :user_id;""")
    orders = db.session.execute(text(sql), {"user_id":user_id}).fetchall()
    for order in orders:
        print(order)
    return orders