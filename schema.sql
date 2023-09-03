CREATE TABLE Users (
    id SERIAL PRIMARY KEY,
    username TEXT,
    password TEXT,
	admin BOOLEAN,
	restaurant BOOLEAN,
	UNIQUE(username)
);

CREATE TABLE Restaurants (
	id SERIAL PRIMARY KEY,
	name TEXT,
	owner_id INTEGER REFERENCES Users,
	UNIQUE(name)
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
    logged_at TIMESTAMP,
	delivered BOOLEAN
);

CREATE TABLE OrderItems (
	id SERIAL PRIMARY KEY,
	order_id INTEGER REFERENCES  Orders,
	menuItem_id INTEGER REFERENCES MenuItems,
	item_name TEXT,
	quantity INTEGER,
	price INTEGER
)