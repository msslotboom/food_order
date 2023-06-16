from flask import Flask
from flask import render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from os import getenv
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.secret_key = getenv("SECRET_KEY")
from db import db
import users, menu

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
    menu_items = menu.get_menu_from_restaurant(restaurant_id)
    restaurant_query = ("SELECT * FROM Restaurants WHERE id=:restaurant_id")
    restaurant = db.session.execute(text(restaurant_query), {"restaurant_id":restaurant_id}).fetchone()
    return render_template("order.html", menu_items=menu_items, restaurant=restaurant)

@app.route("/order/<int:restaurant_id>", methods=["POST"])
def process_order(restaurant_id):
    menu_items = menu.get_menu_from_restaurant(restaurant_id)
    ordered_items = []
    tot_price = 0
    for item in menu_items:
        print(item.id)
        amount = int(request.form[str(item.id)])
        if amount != 0:
            ordered_items.append((item, amount))
        tot_price += item.price * (amount)

    user_id = users.get_id_from_username(session["username"])

    #Create Order in Orders table
    create_order_query = ("INSERT INTO Orders (user_id, restaurant_id, total_price, logged_at) VALUES (:user_id, :restaurant_id, :total_price, :logged_at) RETURNING id")
    order_id = db.session.execute(text(create_order_query), {"user_id": user_id, "restaurant_id": restaurant_id, "total_price": tot_price, "logged_at": datetime.now()}).fetchone()[0]
    print(order_id)
    db.session.commit()

    # Insert each item into OrderItems
    order_item_add_query = ("INSERT INTO OrderItems (order_id, menuItem_id, quantity, price) VALUES (:order_id, :menuItem_id, :quantity, :price)")
    for item in ordered_items:
        print(item)
        db.session.execute(text(order_item_add_query), {"order_id": order_id, "menuItem_id": item[0][0], "quantity":item[1], "price":item[0][1]})
        db.session.commit()
    
    return render_template("result.html",   pizza="a",
                                             message="A")