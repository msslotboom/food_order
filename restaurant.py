from sqlalchemy.sql import text
from db import db

def get_restaurant(id):
    sql = ("SELECT * FROM restaurants WHERE id=:id")
    return db.session.execute(text(sql), {"id":id}).fetchone()

def create_restaurant(restaurant_name):
    sql = ("INSERT INTO restaurants (name) VALUES (:name) RETURNING id")
    restaurant_id = db.session.execute(text(sql), {"name":restaurant_name}).fetchone()[0]
    db.session.commit()
    return restaurant_id