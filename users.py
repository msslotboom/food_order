from werkzeug.security import check_password_hash, generate_password_hash
from flask import Flask
from flask import render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from os import getenv
from db import db

def create_user(username, password):
	sql = "SELECT * FROM users WHERE username=:username"
	check = db.session.execute(text(sql), {"username":username}).fetchone()
	if check is not None:
		return False
	hash_value = generate_password_hash(password)
	sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
	db.session.execute(text(sql), {"username":username, "password":hash_value})
	db.session.commit()

def check_credentials(username, password):
	sql = "SELECT id, password FROM users WHERE username=:username"
	result = db.session.execute(text(sql), {"username": username})
	user = result.fetchone()
	if not user:
		return False
	hash_value = user.password
	if check_password_hash(hash_value, password):
		print("True")
		return True
	return False