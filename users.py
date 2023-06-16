from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text
from db import db

def create_user(username, password):
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


def get_id_from_username(username):
	sql = "SELECT id FROM users WHERE username=:username"
	id = db.session.execute(text(sql), {"username": username}).fetchone()[0]
	if id is not None:
		return id
	return False