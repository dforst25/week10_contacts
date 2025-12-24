-- Create database if it doesn't exist
CREATE DATABASE IF NOT EXISTS contacts_db;

USE contacts_db;

-- Create contacts table
CREATE TABLE IF NOT EXISTS contacts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    phone_number VARCHAR(20) NOT NULL UNIQUE
);

-- Insert sample contacts for testing
INSERT INTO contacts (first_name, last_name, phone_number) VALUES
    ('John', 'Doe', '050-1234567'),
    ('Jane', 'Smith', '052-9876543'),
    ('Bob', 'Johnson', '054-5555555'),
    ('Jack', 'Robinson', '050-6115555');
