from flask import Flask
from flask import render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    restaurants = ["Pizzeria", "Sushi restaurant", "Cafe"]
    return render_template("index.html", restaurants=restaurants)

@app.route("/order")
def order():
    return render_template("order.html")

@app.route("/order", methods=["POST"])
def process_order():
    pizza = request.form["pizza"]
    message = request.form["message"]
    return render_template("result.html",   pizza=pizza,
                                            message=message)