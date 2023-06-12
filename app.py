from flask import Flask
from flask import render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///tsoha"
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
    return render_template("result.html",   pizza=pizza,
                                            message=message)