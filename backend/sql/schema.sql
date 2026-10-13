-- Schema for the e-commerce backend.
-- Reconstructed from the columns the code uses. If you already have a local
-- database, compare it with this file instead of re-running it.
CREATE DATABASE IF NOT EXISTS ecommerce_db;
USE ecommerce_db;

CREATE TABLE IF NOT EXISTS user_details (
    userid    INT AUTO_INCREMENT PRIMARY KEY,
    name      VARCHAR(100) NOT NULL,
    email_id  VARCHAR(255) NOT NULL UNIQUE,
    password  VARCHAR(255) NOT NULL,          -- bcrypt hash (60 chars); 255 leaves room
    role      ENUM('user', 'admin') NOT NULL DEFAULT 'user'
);

CREATE TABLE IF NOT EXISTS products (
    productid INT AUTO_INCREMENT PRIMARY KEY,
    name      VARCHAR(255) NOT NULL,
    category  VARCHAR(100),
    price     DECIMAL(10, 2) NOT NULL,
    image     VARCHAR(500)
);

CREATE TABLE IF NOT EXISTS cart (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    user_id    INT NOT NULL,
    product_id INT NOT NULL,
    name       VARCHAR(255),
    price      DECIMAL(10, 2),
    quantity   INT NOT NULL DEFAULT 1,
    image      VARCHAR(500),
    UNIQUE KEY uniq_user_product (user_id, product_id),
    FOREIGN KEY (user_id) REFERENCES user_details(userid) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(productid) ON DELETE CASCADE
);
