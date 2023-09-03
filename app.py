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
    # print(session["restaurant"])
    restaurants = db.session.execute(text("SELECT * FROM restaurants")).fetchall()
    owned_restaurants = None
    if "username" in session:
        user_is_restaurant = users.is_user_restaurant(session["username"])
        if user_is_restaurant:
            owner_id = users.get_id_from_username(session["username"])
            owned_restaurants = restaurant.get_restaurants_from_owner_id(owner_id)
            print(owned_restaurants)
    else:
        user_is_restaurant = False
    return render_template("index.html", restaurants=restaurants, user_is_restaurant=user_is_restaurant, owned_restaurants=owned_restaurants)

@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    if users.check_credentials(username, password):
        session["username"] = username
        if users.is_user_restaurant(username):
            session["restaurant"] = True
        else:
            session["restaurant"] = False
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
    if users.user_exists(username):
        return render_template("error.html", error="username is already in use! Try another username")
    if password == password_repeat and users.create_user(username, password, restaurant):
        session["username"] = username
        if users.is_user_restaurant(username):
            session["restaurant"] = True
            return redirect("/create_restaurant")
        session["restaurant"] = False
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
    if users.is_user_restaurant(session["username"]):
        return render_template("create_restaurant.html")
    return render_template("error.html", error="Your account is not set up as a restaurant! Create a new account of type restaurant to create a restaurant")

@app.route("/create_restaurant", methods=["POST"])
def create_restaurant():
    if users.is_user_restaurant(session["username"]):
        restaurant_name = request.form["restaurant_name"]
        owner_id = users.get_id_from_username(session["username"])
        restaurant_id = restaurant.create_restaurant(restaurant_name, owner_id)
        return redirect("/create_menu/"+ str(restaurant_id))
    return render_template("error.html", error="Your account is not set up as a restaurant! Create a new account of type restaurant to create a restaurant")

@app.route("/create_menu/<int:restaurant_id>")
def show_create_menu_page(restaurant_id):
    user_id = users.get_id_from_username(session["username"])
    if restaurant.user_is_restaurant_owner(user_id, restaurant_id):
        restaurant_data = restaurant.get_restaurant(restaurant_id)
        menu_items = menu.get_menu_from_restaurant(restaurant_id)
        return render_template("/create_menu.html", restaurant=restaurant_data, menu_items=menu_items)
    return render_template("error.html", error="You do not have permissions to modify this menu!")

@app.route("/create_menu/add/<int:restaurant_id>", methods=["POST"])
def add_menu_item(restaurant_id):
    user_id = users.get_id_from_username(session["username"])
    if restaurant.user_is_restaurant_owner(user_id, restaurant_id):
        item_name = request.form["item_name"]
        description = request.form["description"]
        price = int(request.form["price"])
        menu.add_item(restaurant_id, item_name, description, price)
        return redirect("/create_menu/" + str(restaurant_id))
    return render_template("error.html", error="You do not have permissions to modify this menu!")

@app.route("/create_menu/modify/<int:item_id>", methods=["POST"])
def modify_menu_item(item_id):
    user_id = users.get_id_from_username(session["username"])
    restaurant_id = menu.get_restaurant_id(item_id)
    if restaurant.user_is_restaurant_owner(user_id, restaurant_id) or users.is_admin(user_id):
        item_name = request.form["item_name"]
        description = request.form["description"]
        price = int(request.form["price"])
        menu.modify_item(item_id, item_name, description, price)
        restaurant_id = menu.get_restaurant_id(item_id)
        return redirect("/create_menu/" + str(restaurant_id))
    return render_template("error.html", error="You do not have permissions to modify this menu!")

@app.route("/create_menu/delete/<int:item_id>", methods=["POST"])
def remove_menu_item(item_id):
    user_id = users.get_id_from_username(session["username"])
    restaurant_id = menu.get_restaurant_id(item_id)
    if restaurant.user_is_restaurant_owner(user_id, restaurant_id):
        restaurant_id = menu.get_restaurant_id(item_id)
        menu.remove_item(item_id)
        return redirect("/create_menu/" + str(restaurant_id))
    return render_template("error.html", error="You do not have permissions to modify this menu!")

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
    return redirect("/order_info/" + str(order_id))

@app.route("/order_history/myorders")
def redirect_to_own_orders():
    user_id = users.get_id_from_username(session["username"])
    return redirect("/order_history/" + str(user_id))

@app.route("/order_history/<int:user_id>")
def show_orders(user_id):
    id = users.get_id_from_username(session["username"])
    if id == user_id or users.is_admin(session["username"]):
        orders = order.get_orders_for_user(user_id)
        return render_template("order_history.html", orders=orders)
    return render_template("error.html", error="You do not have permissions to see this page!")

@app.route("/order_info/<int:order_id>")
def order_info(order_id):
    user_id = users.get_id_from_username(session["username"])
    restaurant_id = order.get_restaurant_id_from_order(order_id)
    if order.order_owned_by_user(user_id, order_id) or users.is_admin(session["username"]) or restaurant.user_is_restaurant_owner(user_id, restaurant_id):
        ordered_items = order.get_order_items(order_id)
        print("ordered_items:",ordered_items)
        total_price = order.total_price_of_order(order_id)
        delivery_status = order.get_delivery_status(order_id)
        return render_template("order_info.html", ordered_items=ordered_items, total_price=total_price, delivery_status=delivery_status)
    return render_template("error.html", error="You do not have permissions to see this page!")

@app.route("/manage_orders/<int:restaurant_id>")
def show_all_restaurant_orders(restaurant_id):
    user_id = users.get_id_from_username(session["username"])
    if restaurant.user_is_restaurant_owner(user_id, restaurant_id) or users.is_admin(session["username"]):
        orders = order.get_orders_for_restaurant(restaurant_id)
        restaurant_name = restaurant.get_restaurant(restaurant_id).name
        return render_template("restaurant_orders.html", orders=orders, restaurant_name=restaurant_name)
    return render_template("error.html", error="You do not have permissions to view this site!")

@app.route("/manage_orders/order/<int:order_id>")
def manage_order(order_id):
    user_id = users.get_id_from_username(session["username"])
    restaurant_id = order.get_restaurant_id_from_order(order_id)
    if restaurant.user_is_restaurant_owner(user_id, restaurant_id) or users.is_admin(session["username"]):
        ordered_items = order.get_order_items(order_id)
        print("ordered_items:",ordered_items)
        total_price = order.total_price_of_order(order_id)
        delivery_status = order.get_delivery_status(order_id)
        return render_template("manage_order.html", ordered_items=ordered_items, total_price=total_price, delivery_status=delivery_status, order_id=order_id)
    return render_template("error.html", error="You do not have permissions to view this site!")

@app.route("/manage_orders/set_delivered/<int:order_id>", methods=["POST"])
def set_delivered(order_id):
    user_id = users.get_id_from_username(session["username"])
    restaurant_id = order.get_restaurant_id_from_order(order_id)
    if restaurant.user_is_restaurant_owner(user_id, restaurant_id) or users.is_admin(session["username"]):
        order.set_delivered(order_id)
    return redirect("/manage_orders/order/" + str(order_id))