-- ticket_booking_system.sql
drop database ticketbookingsystem;
-- Create the database
CREATE DATABASE IF NOT EXISTS TicketBookingSystem;
USE TicketBookingSystem;

CREATE TABLE Venue (
    venue_id INT AUTO_INCREMENT PRIMARY KEY,
    venue_name VARCHAR(100) NOT NULL,
    address VARCHAR(255) NOT NULL
);

-- Create Customer table
CREATE TABLE Customer (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    phone_number VARCHAR(20) NOT NULL
);

-- Create Event table
CREATE TABLE Event (
    event_id INT AUTO_INCREMENT PRIMARY KEY,
    event_name VARCHAR(100) NOT NULL,
    event_date DATE NOT NULL,
    event_time TIME NOT NULL,
    venue_id INT NOT NULL,
    total_seats INT NOT NULL,
    available_seats INT NOT NULL,
    ticket_price DECIMAL(10, 2) NOT NULL,
    event_type ENUM('Movie', 'Sports', 'Concert') NOT NULL,
    FOREIGN KEY (venue_id) REFERENCES Venue(venue_id)
);

-- Create Booking table
CREATE TABLE Booking (
    booking_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    event_id INT NOT NULL,
    num_tickets INT NOT NULL,
    total_cost DECIMAL(10, 2) NOT NULL,
    booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id),
    FOREIGN KEY (event_id) REFERENCES Event(event_id)
);

-- Insert sample data into Venue table
INSERT INTO Venue (venue_name, address) VALUES
('Grand Theater', '123 Main St, New York'),
('Sports Arena', '456 Oak Ave, Los Angeles'),
('Concert Hall', '789 Pine Rd, Chicago'),
('Movieplex', '321 Elm Blvd, Houston'),
('Stadium', '654 Maple Dr, Philadelphia');

-- Insert sample data into Customer table
INSERT INTO Customer (customer_name, email, phone_number) VALUES
('John Doe', 'john@example.com', '1234567890'),
('Jane Smith', 'jane@example.com', '2345678901'),
('Bob Johnson', 'bob@example.com', '3456789012'),
('Alice Brown', 'alice@example.com', '4567890123'),
('Charlie Davis', 'charlie@example.com', '5678901234'),
('Diana Evans', 'diana@example.com', '6789012345'),
('Ethan Harris', 'ethan@example.com', '7890123456'),
('Fiona Lee', 'fiona@example.com', '8901234567'),
('George King', 'george@example.com', '9012345678'),
('Hannah Miller', 'hannah@example.com', '0123456789');

-- Insert sample data into Event table
INSERT INTO Event (event_name, event_date, event_time, venue_id, total_seats, available_seats, ticket_price, event_type) VALUES
('Avengers Premiere', '2023-12-15', '18:00:00', 1, 200, 200, 1200.00, 'Movie'),
('World Cup Final', '2023-12-18', '15:00:00', 2, 50000, 50000, 2500.00, 'Sports'),
('Coldplay Concert', '2023-12-20', '20:00:00', 3, 10000, 10000, 3500.00, 'Concert'),
('The Batman', '2023-12-22', '19:30:00', 4, 150, 150, 1000.00, 'Movie'),
('NBA Finals', '2023-12-25', '18:30:00', 5, 20000, 20000, 2000.00, 'Sports'),
('Taylor Swift Tour', '2023-12-28', '19:00:00', 3, 15000, 15000, 4000.00, 'Concert'),
('Jurassic World', '2023-12-30', '17:00:00', 4, 200, 200, 1100.00, 'Movie'),
('Cricket Cup', '2024-01-05', '14:00:00', 2, 30000, 30000, 1800.00, 'Sports'),
('Ed Sheeran Live', '2024-01-10', '20:30:00', 3, 12000, 12000, 3800.00, 'Concert'),
('Black Panther', '2024-01-15', '18:00:00', 1, 180, 180, 1300.00, 'Movie');

-- Insert sample data into Booking table
INSERT INTO Booking (customer_id, event_id, num_tickets, total_cost) VALUES
(1, 1, 2, 2400.00),
(2, 3, 1, 3500.00),
(3, 2, 4, 10000.00),
(4, 5, 2, 4000.00),
(5, 4, 3, 3000.00),
(6, 7, 2, 2200.00),
(7, 6, 1, 4000.00),
(8, 9, 2, 7600.00),
(9, 8, 5, 9000.00),
(10, 10, 2, 2600.00);