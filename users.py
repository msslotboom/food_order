from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text
from db import db

def create_user(username, password, restaurant):
	#TODO: Add password checks
	hash_value = generate_password_hash(password)
	sql = "INSERT INTO users (username, password, admin, restaurant) VALUES (:username, :password, FALSE, :restaurant)"
	db.session.execute(text(sql), {"username":username, "password":hash_value, "restaurant":restaurant})
	db.session.commit()
	return True

def check_credentials(username, password):
	sql = "SELECT password FROM users WHERE username=:username"
	result = db.session.execute(text(sql), {"username": username})
	user = result.fetchone()
	if user is None:
		return False
	hash_value = user.password
	if check_password_hash(hash_value, password):
		return True
	return False

def user_exists(username):
	sql = "SELECT * FROM users WHERE username=:username"
	result = db.session.execute(text(sql), {"username": username})
	username = result.fetchone()
	if username is not None:
		return True
	return False

def get_id_from_username(username):
	sql = "SELECT id FROM users WHERE username=:username"
	id = db.session.execute(text(sql), {"username": username}).fetchone()[0]
	if id is not None:
		return id
	return False

def is_user_restaurant(username):
	sql = "SELECT restaurant FROM users WHERE username=:username"
	restaurant = db.session.execute(text(sql), {"username": username}).fetchone()[0]
	return restaurant

def is_admin(username):
	sql = "SELECT admin FROM users WHERE username=:username"
	admin = db.session.execute(text(sql), {"username":username}).fetchone()[0]
	return admin