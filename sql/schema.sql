-- SQL Schema for Seller Performance Analytics Dashboard

-- Drop tables if they exist
DROP TABLE IF EXISTS returns;
DROP TABLE IF EXISTS ratings;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS sellers;

-- Create Sellers table
CREATE TABLE sellers (
    seller_id VARCHAR(50) PRIMARY KEY,
    seller_name VARCHAR(100) NOT NULL,
    seller_location VARCHAR(100) NOT NULL,
    join_date DATE NOT NULL,
    category_specialization VARCHAR(50)
);

-- Create Orders table
CREATE TABLE orders (
    order_id VARCHAR(50) PRIMARY KEY,
    seller_id VARCHAR(50) NOT NULL,
    order_date DATE NOT NULL,
    shipped_date DATE,
    delivered_date DATE,
    order_status VARCHAR(20) NOT NULL CHECK (order_status IN ('delivered', 'cancelled', 'returned')),
    product_category VARCHAR(50) NOT NULL,
    order_value NUMERIC(10, 2) NOT NULL,
    FOREIGN KEY (seller_id) REFERENCES sellers(seller_id)
);

-- Create Ratings table
CREATE TABLE ratings (
    rating_id VARCHAR(50) PRIMARY KEY,
    order_id VARCHAR(50) NOT NULL,
    seller_id VARCHAR(50) NOT NULL,
    rating_score INTEGER NOT NULL CHECK (rating_score BETWEEN 1 AND 5),
    review_text TEXT,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (seller_id) REFERENCES sellers(seller_id)
);

-- Create Returns table
CREATE TABLE returns (
    return_id VARCHAR(50) PRIMARY KEY,
    order_id VARCHAR(50) NOT NULL UNIQUE,
    seller_id VARCHAR(50) NOT NULL,
    return_reason VARCHAR(200) NOT NULL,
    return_date DATE NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (seller_id) REFERENCES sellers(seller_id)
);

-- Create indexes for better query performance
CREATE INDEX idx_orders_seller_id ON orders(seller_id);
CREATE INDEX idx_orders_order_date ON orders(order_date);
CREATE INDEX idx_orders_product_category ON orders(product_category);
CREATE INDEX idx_ratings_seller_id ON ratings(seller_id);
CREATE INDEX idx_returns_seller_id ON returns(seller_id);
