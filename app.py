from flask import Flask
from flask import render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from os import getenv

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.secret_key = getenv("SECRET_KEY")
from db import db
import users, menu, restaurant, order

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
    restaurant = request.form["restaurant"]
    print(restaurant)
    if password == password_repeat and users.create_user(username, password, restaurant):
        session["username"] = username
        print("Succes")
        if users.is_user_restaurant(username):
            return redirect("/create_restaurant")
        return redirect("/")
    else:
        print("fail")
        return redirect("/create_user")

@app.route("/restaurant/<int:restaurant_id>")
def restaurant_page(restaurant_id):
    restaurant_data = restaurant.get_restaurant(restaurant_id)
    return render_template("restaurant.html", restaurant_name=restaurant_data.name, order_id=restaurant_data.id)

@app.route("/order/<int:restaurant_id>")
def show_order(restaurant_id):
    menu_items = menu.get_menu_from_restaurant(restaurant_id)
    restaurant_data = restaurant.get_restaurant(restaurant_id)
    return render_template("order.html", menu_items=menu_items, restaurant=restaurant_data)

@app.route("/create_restaurant")
def show_create_restaurant_page():
    return render_template("create_restaurant.html")

@app.route("/create_restaurant", methods=["POST"])
def create_restaurant():
    restaurant_name = request.form["restaurant_name"]
    restaurant_id = restaurant.create_restaurant(restaurant_name)
    return redirect("/create_menu/"+ str(restaurant_id))

@app.route("/create_menu/<int:restaurant_id>")
def show_create_menu_page(restaurant_id):
    #TODO: validate if menu is allowed to be modified
    restaurant_data = restaurant.get_restaurant(restaurant_id)
    menu_items = menu.get_menu_from_restaurant(restaurant_id)
    return render_template("/create_menu.html", restaurant=restaurant_data, menu_items=menu_items)

@app.route("/create_menu/add/<int:restaurant_id>", methods=["POST"])
def add_menu_item(restaurant_id):
    #TODO: validate if menu is allowed to be modified
    item_name = request.form["item_name"]
    description = request.form["description"]
    price = int(request.form["price"])
    menu.add_item(restaurant_id, item_name, description, price)
    return redirect("/create_menu/" + str(restaurant_id))

@app.route("/create_menu/modify/<int:item_id>", methods=["POST"])
def modify_menu_item(item_id):
    #TODO: validate if menu is allowed to be modified
    item_name = request.form["item_name"]
    description = request.form["description"]
    price = int(request.form["price"])
    menu.modify_item(item_id, item_name, description, price)
    restaurant_id = menu.get_restaurant_id(item_id)
    return redirect("/create_menu/" + str(restaurant_id))

@app.route("/create_menu/delete/<int:item_id>", methods=["POST"])
def remove_menu_item(item_id):
    #TODO: validate if menu is allowed to be modified
    restaurant_id = menu.get_restaurant_id(item_id)
    menu.remove_item(item_id)
    return redirect("/create_menu/" + str(restaurant_id))

@app.route("/order/<int:restaurant_id>", methods=["POST"])
def process_order(restaurant_id):
    menu_items = menu.get_menu_from_restaurant(restaurant_id)
    ordered_items = []
    tot_price = 0
    for item in menu_items:
        amount = int(request.form[str(item.id)])
        if amount != 0:
            ordered_items.append((item, amount))
        tot_price += item.price * (amount)

    user_id = users.get_id_from_username(session["username"])
    order_id = order.create_order(user_id, restaurant_id, tot_price)
    order.add_order_items(order_id, ordered_items)
    return render_template("order_info.html",   ordered_items=ordered_items, total_price=tot_price)

@app.route("/order_history/myorders")
def redirect_to_own_orders():
    user_id = users.get_id_from_username(session["username"])
    return redirect("/order_history/" + str(user_id))

@app.route("/order_history/<int:user_id>")
def show_orders(user_id):
    #TODO: only access if user_id is logged in user
    orders = order.get_orders(user_id)
    return render_template("order_history.html", orders=orders)