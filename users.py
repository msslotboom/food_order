from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text
from db import db

def create_user(username, password):
	if user_exists(username):
		return False
	#TODO: Add password checks
	hash_value = generate_password_hash(password)
	sql = "INSERT INTO users (username, password, admin) VALUES (:username, :password, FALSE)"
	db.session.execute(text(sql), {"username":username, "password":hash_value})
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
	user = result.fetchone()
	print("User in user_exists function:", user)
	if not user:
		return False
	return True