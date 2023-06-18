from sqlalchemy.sql import text
from db import db

def get_menu_from_restaurant(restaurant_id):
    sql = ("SELECT id, item_name, description, price FROM MenuItems WHERE restaurant_id=:restaurant_id ORDER BY id")
    menu_items = db.session.execute(text(sql), {"restaurant_id":restaurant_id}).fetchall()
    return menu_items

def add_item(restaurant_id, item_name, description, price):
    sql = ("INSERT INTO MenuItems (restaurant_id, item_name, description, price) VALUES (:restaurant_id, :item_name, :description, :price)")
    db.session.execute(text(sql), {"restaurant_id":restaurant_id, "item_name":item_name, "description":description, "price":price})
    db.session.commit()

def modify_item(item_id, item_name, description, price):
    sql = ("UPDATE MenuItems SET item_name=:item_name, description=:description, price=:price WHERE id=:item_id")
    db.session.execute(text(sql), {"item_name":item_name, "description":description, "price":price, "item_id":item_id})
    db.session.commit()

def get_restaurant_id(item_id):
    sql = ("SELECT restaurant_id FROM MenuItems WHERE id=:item_id")
    restaurant_id = db.session.execute(text(sql), {"item_id":item_id}).fetchone()[0]
    print(restaurant_id)
    return restaurant_id