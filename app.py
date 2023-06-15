from flask import Flask
from flask import render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from os import getenv

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.secret_key = getenv("SECRET_KEY")
from db import db
import users

@app.route("/")
def index():
    restaurants = db.session.execute(text("SELECT * FROM restaurants")).fetchall()
    return render_template("index.html", restaurants=restaurants)

@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    if users.check_credentials(username, password):
        session["username"] = username
    return redirect("/")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/create_user")
def show_create_user_page():
    return render_template("create_user.html")

@app.route("/create_user", methods=["POST"])
def create_user():
    username = request.form["username"]
    password = request.form["password"]
    password_repeat = request.form["password_repeat"]
    if password == password_repeat and users.create_user(username, password):
        session["username"] = username
        print("Succes")
        return redirect("/")
    else:
        print("fail")
        return redirect("/create_user")

@app.route("/restaurant/<int:restaurant_id>")
def restaurant_page(restaurant_id):
    sql = ("SELECT id, name FROM restaurants WHERE id=:id")
    restaurant = db.session.execute(text(sql), {"id":restaurant_id}).fetchone()
    return render_template("restaurant.html", restaurant_name=restaurant.name, order_id=restaurant.id)

@app.route("/order/<int:restaurant_id>")
def show_order(restaurant_id):
    sql = ("SELECT item_name, description, price FROM MenuItems WHERE restaurant_id=:restaurant_id")
    menu_items = db.session.execute(text(sql), {"restaurant_id":restaurant_id}).fetchall()
    print(menu_items)
    return render_template("order.html", form=menu_items)

@app.route("/order", methods=["POST"])
def process_order():
    pizza = request.form["pizza"]
    message = request.form["message"]
    sql = "INSERT INTO orders (user_id, restaurant_id, ordered_food, price) VALUES (:user_id, :restaurant_id, :ordered_food, :price)"
    db.session.execute(text(sql), {"user_id":1, "restaurant_id":3, "ordered_food":message, "price":15})
    db.session.commit()
    return render_template("result.html",   pizza=pizza,
                                            message=message)