import mysql.connector
from datetime import datetime

# Database connection function
def connect_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",  # Change to your MySQL username
            password="root",  # Change to your MySQL password
            database="ticketbookingsystem",  # Change to your database name
            autocommit=True  # Enable autocommit to prevent lock issues
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Event class
class Event:
    def __init__(self, event_id):
        self.event_id = event_id
        self.conn = connect_db()
        self.cursor = self.conn.cursor()

    def get_available_tickets(self):
        query = "SELECT available_seats FROM event WHERE event_id = %s"
        self.cursor.execute(query, (self.event_id,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def update_available_tickets(self, new_seats):
        try:
            query = "UPDATE event SET available_seats = %s WHERE event_id = %s"
            self.cursor.execute(query, (new_seats, self.event_id))
            self.conn.commit()  # Ensure changes are committed
        except mysql.connector.Error as err:
            print(f"Error updating tickets: {err}")

# Booking class
class Booking:
    def __init__(self, customer_name, email, phone_number, event_id, num_tickets):
        self.customer_name = customer_name
        self.email = email
        self.phone_number = phone_number
        self.event_id = event_id
        self.num_tickets = num_tickets
        self.conn = connect_db()
        self.cursor = self.conn.cursor()

    def book_tickets(self):
        event = Event(self.event_id)
        available_tickets = event.get_available_tickets()

        if available_tickets is None:
            print("Event not found.")
            return False

        if available_tickets >= self.num_tickets:
            total_cost = self.calculate_cost()

            try:
                # Insert customer details
                customer_query = "INSERT INTO customer (customer_name, email, phone_number) VALUES (%s, %s, %s)"
                self.cursor.execute(customer_query, (self.customer_name, self.email, self.phone_number))
                customer_id = self.cursor.lastrowid

                # Insert booking details
                booking_query = """INSERT INTO booking (customer_id, event_id, num_tickets, total_cost, booking_date) 
                                   VALUES (%s, %s, %s, %s, %s)"""
                self.cursor.execute(booking_query, (customer_id, self.event_id, self.num_tickets, total_cost, datetime.now()))
                booking_id = self.cursor.lastrowid

                # Update available tickets
                event.update_available_tickets(available_tickets - self.num_tickets)

                print(f"Booking successful! Booking ID: {booking_id}, Total Cost: ${total_cost}")
                return True

            except mysql.connector.Error as err:
                print(f"Error during booking: {err}")
                return False
        else:
            print("Tickets unavailable. Not enough seats.")
            return False

    def calculate_cost(self):
        query = "SELECT ticket_price FROM event WHERE event_id = %s"
        self.cursor.execute(query, (self.event_id,))
        result = self.cursor.fetchone()
        if result:
            return self.num_tickets * result[0]
        return 0

# Cancellation class
class Cancellation:
    def __init__(self, booking_id):
        self.booking_id = booking_id
        self.conn = connect_db()
        self.cursor = self.conn.cursor()

    def cancel_ticket(self):
        # Fetch booking details
        query = "SELECT event_id, num_tickets FROM booking WHERE booking_id = %s"
        self.cursor.execute(query, (self.booking_id,))
        booking = self.cursor.fetchone()

        if not booking:
            print("Invalid Booking ID.")
            return False

        event_id, num_tickets = booking

        try:
            # Delete booking
            delete_query = "DELETE FROM booking WHERE booking_id = %s"
            self.cursor.execute(delete_query, (self.booking_id,))

            # Restore seats
            event = Event(event_id)
            available_tickets = event.get_available_tickets()
            event.update_available_tickets(available_tickets + num_tickets)

            print("Booking cancelled successfully.")
            return True

        except mysql.connector.Error as err:
            print(f"Error during cancellation: {err}")
            return False

# Main Program
def main():
    while True:
        print("\nWelcome to the Ticket Booking System")
        print("1. Book Tickets")
        print("2. Cancel Booking")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            customer_name = input("Enter your name: ")
            email = input("Enter your email: ")
            phone_number = input("Enter your phone number: ")
            event_id = int(input("Enter Event ID: "))
            num_tickets = int(input("Enter number of tickets: "))

            booking = Booking(customer_name, email, phone_number, event_id, num_tickets)
            booking.book_tickets()

        elif choice == "2":
            booking_id = int(input("Enter Booking ID to cancel: "))
            cancel = Cancellation(booking_id)
            cancel.cancel_ticket()

        elif choice == "3":
            print("Thank you for using the Ticket Booking System!")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
