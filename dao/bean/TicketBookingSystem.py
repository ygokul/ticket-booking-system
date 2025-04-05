from dao.bean.BookingSystem import BookingSystem
from entity.model.movie import Movie
from entity.model.concert import Concert
from entity.model.sports import Sports
from entity.model.booking import Booking
from entity.model.customer import Customer
from util.db_connection import DBConnUtil
from exception.EventNotFoundException import EventNotFoundException
from exception.InvalidBookingIDException import InvalidBookingIDException
from exception.NullPointerException import NullPointerException

class Admin:
    def __init__(self, conn):
        self.conn = conn

    def create_event(self, event_name, event_date, event_time, venue_id, total_seats, event_type):
        try:
            with self.conn.cursor() as cursor:
                # Insert into Event table
                cursor.execute("""
                    INSERT INTO Event (event_name, event_date, event_time, venue_id, total_seats, available_seats, event_type)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (event_name, event_date, event_time, venue_id, total_seats, total_seats, event_type))
                
                event_id = cursor.lastrowid

                # Prompt for additional info based on event type
                if event_type.lower() == 'movie':
                    genre = input("🎬 Enter Genre: ")
                    actor_name = input("🎭 Enter Actor Name: ")
                    actress_name = input("🎭 Enter Actress Name: ")
                    cursor.execute("""
                        INSERT INTO Movie (event_id, genre, actor_name, actress_name)
                        VALUES (%s, %s, %s, %s)
                    """, (event_id, genre, actor_name, actress_name))

                elif event_type.lower() == 'concert':
                    artist = input("🎤 Enter Artist Name: ")
                    concert_type = input("🎵 Enter Concert Type (e.g., Solo, Band, Festival): ")
                    cursor.execute("""
                        INSERT INTO Concert (event_id, artist, concert_type)
                        VALUES (%s, %s, %s)
                    """, (event_id, artist, concert_type))

                elif event_type.lower() == 'sports':
                    sport_name = input("🏅 Enter Sport Name: ")
                    teams_name = input("🏆 Enter Teams (e.g., Team A vs Team B): ")
                    cursor.execute("""
                        INSERT INTO Sports (event_id, sport_name, teams_name)
                        VALUES (%s, %s, %s)
                    """, (event_id, sport_name, teams_name))

            self.conn.commit()
            print(f"\n✅ Event '{event_name}' created successfully with ID {event_id}!")

        except Exception as e:
            self.conn.rollback()
            print(f"❌ Failed to create event: {e}")

    def update_event(self, event_id, event_name, event_date, event_time, venue_id, total_seats, available_seats):
        """Updates event details in Event table and synchronizes changes with Movie, Concert, or Sports tables"""
        with self.conn.cursor() as cursor:
            cursor.execute("""
                UPDATE Event
                SET event_name = %s, event_date = %s, event_time = %s, 
                    venue_id = %s, total_seats = %s, available_seats = %s
                WHERE event_id = %s
            """, (event_name, event_date, event_time, venue_id, total_seats, available_seats, event_id))

            cursor.execute("SELECT event_type FROM Event WHERE event_id = %s", (event_id,))
            result = cursor.fetchone()

            if result:
                event_type = result[0].lower()

                if event_type == "movie":
                    genre = input("Enter genre: ")
                    actor_name = input("Enter actor name: ")
                    actress_name = input("Enter actress name: ")

                    cursor.execute("""
                        UPDATE Movie 
                        SET genre = %s, actor_name = %s, actress_name = %s 
                        WHERE event_id = %s
                    """, (genre, actor_name, actress_name, event_id))

                elif event_type == "concert":
                    artist = input("Enter artist name: ")
                    concert_type = input("Enter concert type: ")

                    cursor.execute("""
                        UPDATE Concert 
                        SET artist = %s, concert_type = %s 
                        WHERE event_id = %s
                    """, (artist, concert_type, event_id))

                elif event_type == "sports":
                    sport_name = input("Enter sport name: ")
                    teams_name = input("Enter new teams: ")

                    cursor.execute("""
                        UPDATE Sports 
                        SET sport_name = %s, teams_name = %s 
                        WHERE event_id = %s
                    """, (sport_name, teams_name, event_id))

        self.conn.commit()
        print(f"✅ Event ID {event_id} updated successfully!")

    def calculate_total_revenue(self, event_id):
        """Calculates total revenue based on ticket sales"""
        price_mapping = {"Silver": 200, "Gold": 500, "Diamond": 1000}
        with self.conn.cursor() as cursor:
            cursor.execute("""
                SELECT ticket_category, SUM(num_tickets)
                FROM Booking
                WHERE event_id = %s
                GROUP BY ticket_category
            """, (event_id,))
            total_revenue = sum(price_mapping[category] * num_tickets for category, num_tickets in cursor.fetchall())
        return total_revenue  

    def get_event_statistics(self, event_id):
        """Returns total booked tickets, remaining tickets, and total revenue"""
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT SUM(num_tickets) FROM Booking WHERE event_id = %s", (event_id,))
            booked_tickets = cursor.fetchone()[0] or 0  

            cursor.execute("SELECT available_seats FROM Event WHERE event_id = %s", (event_id,))
            remaining_tickets = cursor.fetchone()[0] or 0  

            total_revenue = self.calculate_total_revenue(event_id)
        return booked_tickets, remaining_tickets, total_revenue


class TicketBookingSystem(BookingSystem):
    def __init__(self, conn=None):
        if conn is None:
            raise NullPointerException("Database connection is null")
        self.conn = conn
        self.events = []
        self.bookings = []

    def create_event(self, event_id):
        if self.conn is None:
            raise NullPointerException("Database connection is null")
        
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("SELECT event_name, event_date, venue_id, total_seats, event_type FROM Event WHERE event_id = %s", (event_id,))
                result = cursor.fetchone()
                
            if result:
                event_name, event_date, venue_id, total_seats, event_type = result
                if event_type.lower() == "movie":
                    event = Movie(event_id, self.conn)
                elif event_type.lower() == "concert":
                    event = Concert(event_id, self.conn)
                elif event_type.lower() == "sports":
                    event = Sports(event_id, self.conn)
                else:
                    event = None

                if event:
                    self.events.append(event)
                    return event
            else:
                raise EventNotFoundException(f"Event with ID {event_id} not found.")
        except Exception as e:
            print(f"Error creating event: {e}")
        return None

    def display_event_details(self, event):
        event.display_event_details()

    def book_tickets(self, event_id, customer_id, num_tickets, ticket_category):
        try:
            event = next((e for e in self.events if e.event_id == event_id), None)
            if not event:
                event = self.create_event(event_id)
            if event and event.available_seats >= num_tickets:
                total_cost = self.calculate_booking_cost(num_tickets, ticket_category)
                customer = Customer(customer_id)
                booking = Booking(customer, event, num_tickets, ticket_category)
                self.bookings.append(booking)
                event.available_seats -= num_tickets

                # Update database
                with self.conn.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO Booking (booking_id, customer_id, event_id, num_tickets, ticket_category, total_cost, booking_date)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """, (booking.booking_id, customer_id, event_id, num_tickets, ticket_category, total_cost, booking.booking_date))
                    cursor.execute("UPDATE Event SET available_seats = %s WHERE event_id = %s", (event.available_seats, event_id))
                    self.conn.commit()

                return booking.booking_id
            else:
                raise EventNotFoundException(f"Event with ID {event_id} not found or not enough available seats!")
        except Exception as e:
            print(f"Error booking tickets: {e}")
            self.conn.rollback()
            return None

    def cancel_booking(self, booking_id):
        try:
            booking = next((b for b in self.bookings if b.booking_id == booking_id), None)
            if booking:
                booking.event.available_seats += booking.num_tickets
                self.bookings.remove(booking)

                # Update database
                with self.conn.cursor() as cursor:
                    cursor.execute("DELETE FROM Booking WHERE booking_id = %s", (booking_id,))
                    cursor.execute("UPDATE Event SET available_seats = %s WHERE event_id = %s", (booking.event.available_seats, booking.event.event_id))
                    self.conn.commit()

                return booking.booking_id
            else:
                raise InvalidBookingIDException(f"Booking with ID {booking_id} not found!")
        except Exception as e:
            print(f"Error canceling booking: {e}")
            self.conn.rollback()
            return None

    def get_available_seats(self, event_id):
        try:
            event = next((e for e in self.events if e.event_id == event_id), None)
            if not event:
                event = self.create_event(event_id)
            if event:
                return event.available_seats
            else:
                raise EventNotFoundException(f"Event with ID {event_id} not found!")
        except Exception as e:
            print(f"Error getting available seats: {e}")
            return None

    def calculate_booking_cost(self, num_tickets, ticket_category):
        price_mapping = {"Silver": 200, "Gold": 500, "Diamond": 1000}
        return num_tickets * price_mapping.get(ticket_category, 0)

    def get_booking_details(self, booking_id):
        try:
            booking = next((b for b in self.bookings if b.booking_id == booking_id), None)
            if booking:
                return booking.display_booking_details()
            else:
                raise InvalidBookingIDException(f"Booking with ID {booking_id} not found!")
        except Exception as e:
            print(f"Error getting booking details: {e}")
            return None