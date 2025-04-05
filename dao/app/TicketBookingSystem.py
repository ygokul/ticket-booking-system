from util.db_connection import DBConnUtil
from bean.TicketBookingSystem import TicketBookingSystem
from entity.model.venue import Venue
from entity.model.customer import Customer

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

def main():
    conn = DBConnUtil.get_db_connection()
    if not conn:
        print("❌ Database connection failed!")
        return

    booking_system = TicketBookingSystem(conn)
    admin_system = Admin(conn)

    try:
        while True:
            print("\n===== Ticket Booking System =====")
            print("1. Admin Functions")
            print("2. Customer Functions")
            print("3. Exit")
            choice = input("Enter your choice (1-3): ").strip()

            if choice == "1":  # Admin Functions
                admin_command = input("\nAdmin command (create_event, update_event, event_stats, exit): ").strip().lower()
                
                if admin_command == "create_event":
                    event_name = input("Event Name: ")
                    event_date = input("Event Date (YYYY-MM-DD): ")
                    event_time = input("Event Time (HH:MM:SS): ")
                    venue_id = int(input("Venue ID: "))
                    total_seats = int(input("Total Seats: "))
                    event_type = input("Event Type (Movie, Concert, Sports): ").capitalize()
                    
                    admin_system.create_event(event_name, event_date, event_time, venue_id, total_seats, event_type)

                elif admin_command == "update_event":
                    event_id = int(input("Event ID to update: "))
                    event_name = input("New Event Name (leave blank to keep current): ")
                    event_date = input("New Event Date (YYYY-MM-DD, leave blank to keep current): ")
                    event_time = input("New Event Time (HH:MM:SS, leave blank to keep current): ")
                    venue_id = input("New Venue ID (leave blank to keep current): ")
                    total_seats = input("New Total Seats (leave blank to keep current): ")
                    available_seats = input("New Available Seats (leave blank to keep current): ")
                    
                    # Get current values for fields left blank
                    with conn.cursor() as cursor:
                        cursor.execute("SELECT * FROM Event WHERE event_id = %s", (event_id,))
                        current = cursor.fetchone()
                    
                    if not current:
                        print("❌ Event not found!")
                        continue
                        
                    event_name = event_name if event_name else current[1]
                    event_date = event_date if event_date else current[2]
                    event_time = event_time if event_time else current[3]
                    venue_id = int(venue_id) if venue_id else current[4]
                    total_seats = int(total_seats) if total_seats else current[5]
                    available_seats = int(available_seats) if available_seats else current[6]
                    
                    admin_system.update_event(event_id, event_name, event_date, event_time, 
                                            venue_id, total_seats, available_seats)

                elif admin_command == "event_stats":
                    event_id = int(input("Event ID for statistics: "))
                    booked, remaining, revenue = admin_system.get_event_statistics(event_id)
                    print(f"\n📊 Event Statistics for ID {event_id}:")
                    print(f"Booked Tickets: {booked}")
                    print(f"Remaining Tickets: {remaining}")
                    print(f"Total Revenue: ₹{revenue}")

                elif admin_command == "exit":
                    continue

                else:
                    print("❌ Invalid admin command!")

            elif choice == "2":  # Customer Functions
                customer_command = input("\nCustomer command (book_tickets, cancel_booking, available_seats, event_details, exit): ").strip().lower()
                
                if customer_command == "book_tickets":
                    event_id = int(input("Event ID: "))
                    customer_id = int(input("Customer ID: "))
                    num_tickets = int(input("Number of Tickets: "))
                    print("Ticket Categories: Silver(₹200), Gold(₹500), Diamond(₹1000)")
                    ticket_category = input("Ticket Category: ").capitalize()
                    
                    booking_id = booking_system.book_tickets(event_id, customer_id, num_tickets, ticket_category)
                    if booking_id:
                        print(f"✅ Tickets booked successfully! Booking ID: {booking_id}")
                    else:
                        print("❌ Failed to book tickets!")

                elif customer_command == "cancel_booking":
                    booking_id = int(input("Booking ID to cancel: "))
                    if booking_system.cancel_booking(booking_id):
                        print("✅ Booking cancelled successfully!")
                    else:
                        print("❌ Failed to cancel booking!")

                elif customer_command == "available_seats":
                    event_id = int(input("Event ID: "))
                    seats = booking_system.get_available_seats(event_id)
                    if seats is not None:
                        print(f"Available seats: {seats}")
                    else:
                        print("❌ Event not found!")

                elif customer_command == "event_details":
                    event_id = int(input("Event ID: "))
                    event = booking_system.create_event(event_id)
                    if event:
                        booking_system.display_event_details(event)
                    else:
                        print("❌ Event not found!")

                elif customer_command == "exit":
                    continue

                else:
                    print("❌ Invalid customer command!")

            elif choice == "3":  # Exit
                print("👋 Exiting the system. Goodbye!")
                break

            else:
                print("❌ Invalid choice! Please enter 1, 2, or 3.")

    finally:
        conn.close()

if __name__ == "__main__":
    main()