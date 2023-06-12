CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT,
    password TEXT,
	admin BOOLEAN
);

CREATE TABLE restaurants (
	id SERIAL PRIMARY KEY,
	name TEXT
)
CREATE TABLE forms (
    id SERIAL PRIMARY KEY,
	restaurant_id INTEGER REFERENCES restaurants,
    fields TEXT
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
	restaurant_id INTEGER REFERENCES restaurants,
    order TEXT,
	price INTEGER,
    logged_at TIMESTAMP
);