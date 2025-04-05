CREATE DATABASE TicketBookingSystem;
USE TicketBookingSystem;

-- Venue Table
CREATE TABLE Venue (
    venue_id INT PRIMARY KEY AUTO_INCREMENT,
    venue_name VARCHAR(255) NOT NULL,
    address TEXT NOT NULL
);

INSERT INTO Venue (venue_name, address) VALUES ('Royal Theater', '123 Main St, New York, NY 10001');
INSERT INTO Venue (venue_name, address) VALUES ('Olympic Stadium', '456 Elm St, Los Angeles, CA 90001');
INSERT INTO Venue (venue_name, address) VALUES ('Grand Concert Hall', '789 Oak St, Chicago, IL 60601');
INSERT INTO Venue (venue_name, address) VALUES ('City Playhouse', '101 Pine St, Boston, MA 02101');
INSERT INTO Venue (venue_name, address) VALUES ('Metropolitan Arena', '202 Maple St, Miami, FL 33101');
INSERT INTO Venue (venue_name, address) VALUES ('Downtown Exhibition Center', '303 Cedar St, Seattle, WA 98101');
INSERT INTO Venue (venue_name, address) VALUES ('Central Park Amphitheater', '404 Birch St, San Francisco, CA 94101');
INSERT INTO Venue (venue_name, address) VALUES ('Sunset Pavilion', '505 Spruce St, Austin, TX 73301');
INSERT INTO Venue (venue_name, address) VALUES ('Riverside Auditorium', '606 Willow St, Denver, CO 80201');
INSERT INTO Venue (venue_name, address) VALUES ('Harborview Hall', '707 Ash St, San Diego, CA 92101');
-- Event Table
CREATE TABLE Event (
    event_id INT PRIMARY KEY AUTO_INCREMENT,
    event_name VARCHAR(255) NOT NULL,
    event_date DATE NOT NULL,
    event_time TIME NOT NULL,
    venue_id INT NOT NULL,
    total_seats INT NOT NULL,
    available_seats INT NOT NULL,
    event_type ENUM('Movie', 'Sports', 'Concert') NOT NULL,
    FOREIGN KEY (venue_id) REFERENCES Venue(venue_id)
);

-- Insert queries for Event table
INSERT INTO Event (event_name, event_date, event_time, venue_id, total_seats, available_seats, event_type) 
VALUES ('Avengers Movie Premiere', '2025-05-01', '18:00:00', 1, 200, 200, 'Movie');
INSERT INTO Event (event_name, event_date, event_time, venue_id, total_seats, available_seats, event_type) 
VALUES ('NBA Finals', '2025-06-15', '20:00:00', 2, 50000, 50000, 'Sports');
INSERT INTO Event (event_name, event_date, event_time, venue_id, total_seats, available_seats, event_type) 
VALUES ('Coldplay Concert', '2025-07-20', '19:00:00', 3, 15000, 15000, 'Concert');
INSERT INTO Event (event_name, event_date, event_time, venue_id, total_seats, available_seats, event_type) 
VALUES ('Taylor Swift Concert', '2025-08-10', '19:30:00', 3, 15000, 15000, 'Concert');
INSERT INTO Event (event_name, event_date, event_time, venue_id, total_seats, available_seats, event_type) 
VALUES ('UFC Championship', '2025-09-05', '21:00:00', 2, 20000, 20000, 'Sports');
INSERT INTO Event (event_name, event_date, event_time, venue_id, total_seats, available_seats, event_type) 
VALUES ('The Lion King Musical', '2025-10-01', '17:00:00', 1, 300, 300, 'Movie');
INSERT INTO Event (event_name, event_date, event_time, venue_id, total_seats, available_seats, event_type) 
VALUES ('Jazz Festival', '2025-11-12', '18:30:00', 3, 5000, 5000, 'Concert');
INSERT INTO Event (event_name, event_date, event_time, venue_id, total_seats, available_seats, event_type) 
VALUES ('Baseball World Series', '2025-10-18', '19:00:00', 2, 40000, 40000, 'Sports');
INSERT INTO Event (event_name, event_date, event_time, venue_id, total_seats, available_seats, event_type) 
VALUES ('Rock Band Showdown', '2025-12-25', '20:00:00', 3, 8000, 8000, 'Concert');
INSERT INTO Event (event_name, event_date, event_time, venue_id, total_seats, available_seats, event_type) 
VALUES ('Star Wars Marathon', '2025-11-05', '15:00:00', 1, 250, 250, 'Movie');
-- Customer Table
CREATE TABLE Customer (
    customer_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone_number VARCHAR(20) UNIQUE NOT NULL
);
-- Insert queries for Customer table
INSERT INTO Customer (customer_name, email, phone_number) VALUES ('John Doe', 'john.doe@example.com', '1234567890');
INSERT INTO Customer (customer_name, email, phone_number) VALUES ('Jane Smith', 'jane.smith@example.com', '0987654321');
INSERT INTO Customer (customer_name, email, phone_number) VALUES ('Alice Johnson', 'alice.johnson@example.com', '1122334455');
INSERT INTO Customer (customer_name, email, phone_number) VALUES ('Robert Brown', 'robert.brown@example.com', '2233445566');
INSERT INTO Customer (customer_name, email, phone_number) VALUES ('Emily Davis', 'emily.davis@example.com', '3344556677');
INSERT INTO Customer (customer_name, email, phone_number) VALUES ('Michael Wilson', 'michael.wilson@example.com', '4455667788');
INSERT INTO Customer (customer_name, email, phone_number) VALUES ('Sarah Miller', 'sarah.miller@example.com', '5566778899');
INSERT INTO Customer (customer_name, email, phone_number) VALUES ('David Anderson', 'david.anderson@example.com', '6677889900');
INSERT INTO Customer (customer_name, email, phone_number) VALUES ('Laura Thomas', 'laura.thomas@example.com', '7788990011');
INSERT INTO Customer (customer_name, email, phone_number) VALUES ('James Martinez', 'james.martinez@example.com', '8899001122');
-- Booking Table
CREATE TABLE Booking (
    booking_id INT(20) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    customer_id INT NOT NULL,
    event_id INT NOT NULL,
    num_tickets INT NOT NULL,
    ticket_category ENUM('Silver', 'Gold', 'Diamond') NOT NULL,
    total_cost DECIMAL(10,2) NOT NULL,
    booking_date DATE NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id) ON DELETE CASCADE,
    FOREIGN KEY (event_id) REFERENCES Event(event_id) ON DELETE CASCADE
);
-- Insert queries for Booking table
INSERT INTO Booking (customer_id, event_id, num_tickets, ticket_category, total_cost, booking_date) 
VALUES (1, 1, 2, 'Gold', 50.00, '2025-04-05');
INSERT INTO Booking (customer_id, event_id, num_tickets, ticket_category, total_cost, booking_date) 
VALUES (2, 2, 4, 'Silver', 100.00, '2025-04-05');
INSERT INTO Booking (customer_id, event_id, num_tickets, ticket_category, total_cost, booking_date) 
VALUES (3, 3, 3, 'Diamond', 150.00, '2025-04-05');
INSERT INTO Booking (customer_id, event_id, num_tickets, ticket_category, total_cost, booking_date) 
VALUES (4, 4, 1, 'Gold', 25.00, '2025-04-05');
INSERT INTO Booking (customer_id, event_id, num_tickets, ticket_category, total_cost, booking_date) 
VALUES (5, 5, 2, 'Silver', 50.00, '2025-04-05');
INSERT INTO Booking (customer_id, event_id, num_tickets, ticket_category, total_cost, booking_date) 
VALUES (6, 6, 4, 'Diamond', 200.00, '2025-04-05');
INSERT INTO Booking (customer_id, event_id, num_tickets, ticket_category, total_cost, booking_date) 
VALUES (7, 7, 5, 'Gold', 75.00, '2025-04-05');
INSERT INTO Booking (customer_id, event_id, num_tickets, ticket_category, total_cost, booking_date) 
VALUES (8, 8, 3, 'Silver', 75.00, '2025-04-05');
INSERT INTO Booking (customer_id, event_id, num_tickets, ticket_category, total_cost, booking_date) 
VALUES (9, 9, 1, 'Diamond', 50.00, '2025-04-05');
INSERT INTO Booking (customer_id, event_id, num_tickets, ticket_category, total_cost, booking_date) 
VALUES (10, 10, 2, 'Gold', 100.00, '2025-04-05');
-- Movie Table
CREATE TABLE Movie (
    movie_id INT PRIMARY KEY AUTO_INCREMENT,
    event_id INT UNIQUE,
    genre VARCHAR(50) NOT NULL,
    actor_name VARCHAR(100) NOT NULL,
    actress_name VARCHAR(100) NOT NULL,
    FOREIGN KEY (event_id) REFERENCES Event(event_id) ON DELETE CASCADE
);



-- Concert Table
CREATE TABLE Concert (
    concert_id INT PRIMARY KEY AUTO_INCREMENT,
    event_id INT UNIQUE NOT NULL,
    artist VARCHAR(255) NOT NULL,
    concert_type VARCHAR(100) NOT NULL,
    FOREIGN KEY (event_id) REFERENCES Event(event_id) ON DELETE CASCADE
);

-- Sports Table
CREATE TABLE Sports (
    sports_id INT PRIMARY KEY AUTO_INCREMENT,
    event_id INT UNIQUE NOT NULL,
    sport_name VARCHAR(100) NOT NULL,
    team_a VARCHAR(100) NOT NULL,
    team_b VARCHAR(100) NOT NULL,
    match_type VARCHAR(100) NOT NULL,
    FOREIGN KEY (event_id) REFERENCES Event(event_id) ON DELETE CASCADE
);

-- Insert queries for Movie table
INSERT INTO Movie (event_id, genre, actor_name, actress_name) VALUES (1, 'Action', 'Robert Downey Jr.', 'Scarlett Johansson');
INSERT INTO Movie (event_id, genre, actor_name, actress_name) VALUES (6, 'Musical', 'Simba', 'Nala');
INSERT INTO Movie (event_id, genre, actor_name, actress_name) VALUES (11, 'Science Fiction', 'Mark Hamill', 'Carrie Fisher');

-- Insert queries for Concert table
INSERT INTO Concert (event_id, artist, concert_type) VALUES (3, 'Coldplay', 'Rock');
INSERT INTO Concert (event_id, artist, concert_type) VALUES (4, 'Taylor Swift', 'Pop');
INSERT INTO Concert (event_id, artist, concert_type) VALUES (7, 'Various Artists', 'Jazz');
INSERT INTO Concert (event_id, artist, concert_type) VALUES (10, 'Various Bands', 'Rock');

-- Insert queries for Sports table
INSERT INTO Sports (event_id, sport_name, team_a, team_b, match_type) VALUES (2, 'Basketball', 'Team A', 'Team B', 'NBA Finals');
INSERT INTO Sports (event_id, sport_name, team_a, team_b, match_type) VALUES (5, 'Mixed Martial Arts', 'Fighter A', 'Fighter B', 'Championship');
INSERT INTO Sports (event_id, sport_name, team_a, team_b, match_type) VALUES (9, 'Baseball', 'Team A', 'Team B', 'World Series');