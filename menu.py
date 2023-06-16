from sqlalchemy.sql import text
from db import db

def get_menu_from_restaurant(restaurant_id):
    menu_query = ("SELECT id, item_name, description, price FROM MenuItems WHERE restaurant_id=:restaurant_id")
    menu_items = db.session.execute(text(menu_query), {"restaurant_id":restaurant_id}).fetchall()
    return menu_items