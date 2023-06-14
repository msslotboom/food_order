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
    print(restaurants)
    return render_template("index.html", restaurants=restaurants)

@app.route("/restaurant/<int:restaurant_id>")
def restaurant_page(restaurant_id):
    name_sql = ("SELECT name FROM restaurants WHERE id=:id")
    order_sql = ("SELECT id FROM forms WHERE restaurant_id=:restaurant_id")
    name = db.session.execute(text(name_sql), {"id":restaurant_id}).fetchone()[0]
    order_id = db.session.execute(text(order_sql), {"restaurant_id":restaurant_id}).fetchone()[0]
    print(name, order_id)
    return render_template("restaurant.html", restaurant_name=name, order_id=order_id)

@app.route("/order/<int:order_id>")
def order(order_id):
    sql = ("SELECT fields FROM forms WHERE id=:id")
    form = db.session.execute(text(sql), {"id":order_id}).fetchone()[0].split(";")
    print(form)
    return render_template("order.html", form=form)

@app.route("/order", methods=["POST"])
def process_order():
    pizza = request.form["pizza"]
    message = request.form["message"]
    sql = "INSERT INTO orders (user_id, restaurant_id, ordered_food, price) VALUES (:user_id, :restaurant_id, :ordered_food, :price)"
    db.session.execute(text(sql), {"user_id":1, "restaurant_id":3, "ordered_food":message, "price":15})
    db.session.commit()
    return render_template("result.html",   pizza=pizza,
                                            message=message)