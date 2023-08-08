from sqlalchemy.sql import text
from db import db

def get_restaurant(id):
    sql = ("SELECT * FROM restaurants WHERE id=:id")
    return db.session.execute(text(sql), {"id":id}).fetchone()

def create_restaurant(restaurant_name, owner_id):
    sql = ("INSERT INTO restaurants (name, owner_id) VALUES (:name, :owner_id) RETURNING id")
    restaurant_id = db.session.execute(text(sql), {"name":restaurant_name, "owner_id":owner_id}).fetchone()[0]
    db.session.commit()
    return restaurant_id

def get_restaurants_from_owner_id(user_id):
    sql = ("SELECT * FROM restaurants WHERE owner_id=:owner_id")
    restaurant_id = db.session.execute(text(sql), {"owner_id":user_id}).fetchall()
    return restaurant_id