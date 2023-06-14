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