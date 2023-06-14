from flask import Flask
from flask import render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from os import getenv

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)

@app.route("/")
def index():
    result = db.session.execute(text("SELECT name FROM restaurants"))
    restaurants = result.fetchall()
    return render_template("index.html", restaurants=restaurants)

@app.route("/order")
def order():
    return render_template("order.html")

@app.route("/order", methods=["POST"])
def process_order():
    pizza = request.form["pizza"]
    message = request.form["message"]
    sql = "INSERT INTO orders (user_id, restaurant_id, ordered_food, price) VALUES (:user_id, :restaurant_id, :ordered_food, :price)"
    db.session.execute(text(sql), {"user_id":1, "restaurant_id":3, "ordered_food":message, "price":15})
    db.session.commit()
    return render_template("result.html",   pizza=pizza,
                                            message=message)