from sqlalchemy.sql import text
from db import db

def get_restaurant(id):
    sql = ("SELECT * FROM restaurants WHERE id=:id")
    return db.session.execute(text(sql), {"id":id}).fetchone()