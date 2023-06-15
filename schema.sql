CREATE TABLE Users (
    id SERIAL PRIMARY KEY,
    username TEXT,
    password TEXT,
	admin BOOLEAN
);

CREATE TABLE Restaurants (
	id SERIAL PRIMARY KEY,
	name TEXT
);

CREATE TABLE MenuItems (
    id SERIAL PRIMARY KEY,
	restaurant_id INTEGER REFERENCES Restaurants,
    item_name TEXT,
	description TEXT,
	price INTEGER
);

CREATE TABLE Orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES Users,
	restaurant_id INTEGER REFERENCES Restaurants,
	total_price INTEGER,
    logged_at TIMESTAMP
);

CREATE TABLE OrderItems (
	id SERIAL PRIMARY KEY,
	order_id INTEGER REFERENCES  Orders,
	menuItem_id INTEGER REFERENCES MenuItems,
	quantity INTEGER,
	price INTEGER
)