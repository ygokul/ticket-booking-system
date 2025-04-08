from util.db_connection import DBConnUtil
from dao.bean.TicketBookingSystem import TicketBookingSystem
from exception.EventNotFoundException import EventNotFoundException
from exception.InvalidBookingIDException import InvalidBookingIDException
from exception.NullPointerException import NullPointerException

class Admin:
    def __init__(self, conn):
        self.conn = conn

    def create_event(self):
        try:
            print("\n🎭 Create New Event")
            event_name = input("Enter event name: ").strip()
            event_date = input("Enter event date (YYYY-MM-DD): ").strip()
            event_time = input("Enter event time (HH:MM:SS): ").strip()
            venue_id = input("Enter venue ID: ").strip()
            total_seats = input("Enter total seats: ").strip()
            event_type = input("Enter event type (Movie/Concert/Sports): ").strip().capitalize()

            with self.conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO Event (event_name, event_date, event_time, venue_id, total_seats, available_seats, event_type)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (event_name, event_date, event_time, venue_id, total_seats, total_seats, event_type))
                
                event_id = cursor.lastrowid

                if event_type.lower() == 'movie':
                    genre = input("🎬 Enter genre: ")
                    actor_name = input("🎭 Enter lead actor name: ")
                    actress_name = input("🎭 Enter lead actress name: ")
                    cursor.execute("""
                        INSERT INTO Movie (event_id, genre, actor_name, actress_name)
                        VALUES (%s, %s, %s, %s)
                    """, (event_id, genre, actor_name, actress_name))

                elif event_type.lower() == 'concert':
                    artist = input("🎤 Enter artist name: ")
                    concert_type = input("🎵 Enter concert type (Solo/Band/Festival): ")
                    cursor.execute("""
                        INSERT INTO Concert (event_id, artist, concert_type)
                        VALUES (%s, %s, %s)
                    """, (event_id, artist, concert_type))

                elif event_type.lower() == 'sports':
                    sport_name = input("⚽ Enter sport name: ")
                    teams_name = input("🏆 Enter competing teams (e.g., Team A vs Team B): ")
                    cursor.execute("""
                        INSERT INTO Sports (event_id, sport_name, teams_name)
                        VALUES (%s, %s, %s)
                    """, (event_id, sport_name, teams_name))

            self.conn.commit()
            print(f"\n✅ Event '{event_name}' created successfully with ID {event_id}!")

        except Exception as e:
            self.conn.rollback()
            print(f"❌ Failed to create event: {e}")

def display_main_menu():
    print("\n" + "="*50)
    print("🎟 TICKET BOOKING SYSTEM".center(50))
    print("="*50)
    print("1. 🎭 Book Tickets")
    print("2. 🛠 Admin Panel")
    print("3. 🚪 Exit")
    print("="*50)

def handle_customer_booking(conn):
    system = TicketBookingSystem(conn)
    
    try:
        print("\n🔹 Welcome to Ticket Booking 🔹")
        email = input("Enter your email: ").strip()
        
        with conn.cursor() as cursor:
            cursor.execute("SELECT customer_id, customer_name FROM Customer WHERE email = %s", (email,))
            result = cursor.fetchone()

            if result:
                customer_id, customer_name = result
                print(f"\n✅ Welcome back, {customer_name}!")
            else:
                print("\n📝 New user detected. Please register:")
                customer_name = input("Enter your full name: ").strip()
                phone_number = input("Enter your phone number: ").strip()
                
                cursor.execute("""
                    INSERT INTO Customer (customer_name, email, phone_number)
                    VALUES (%s, %s, %s)
                """, (customer_name, email, phone_number))
                conn.commit()
                customer_id = cursor.lastrowid
                print("✅ Registration successful!")

        while True:
            try:
                with conn.cursor() as cursor:
                    # Fetch distinct event types from the database
                    cursor.execute("SELECT DISTINCT event_type FROM Event")
                    event_types = cursor.fetchall()

                if not event_types:
                    print("\n❌ No event types available in the system!")
                    break

                print("\n🎭 Available Event Types:")
                event_type_mapping = {}
                for idx, (event_type,) in enumerate(event_types, 1):
                    print(f"{idx}. {event_type}")
                    event_type_mapping[idx] = event_type

                print(f"{len(event_types) + 1}. ↩ Back to main menu")

                choice = input("Select event type: ").strip()

                if choice.isdigit():
                    choice = int(choice)
                    if choice == len(event_types) + 1:
                        break
                    elif choice in event_type_mapping:
                        selected_event_type = event_type_mapping[choice]
                        print(f"\n🔹 You selected: {selected_event_type}")
                        # Proceed with handling the selected event type
                    else:
                        print("❌ Invalid selection! Please try again.")
                else:
                    print("❌ Invalid input! Please enter a number.")

            except Exception as e:
                print(f"❌ An error occurred: {e}")

            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT event_id, event_name, event_date, event_time, available_seats 
                    FROM Event 
                    WHERE event_type = %s
                """, (selected_event_type,))
                events = cursor.fetchall()

            if not events:
                print(f"\n❌ No available {selected_event_type} events found!")
                continue

            print(f"\n🎟 Available {selected_event_type} Events:")
            for idx, event in enumerate(events, 1):
                print(f"{idx}. {event[1]} (ID: {event[0]})")
                print(f"   📅 Date: {event[2]} ⏰ Time: {event[3]}")
                print(f"   🪑 Available seats: {event[4]}\n")

            event_choice = input("Enter event number to view details (or 'back' to return): ").strip()
            
            if event_choice.lower() == 'back':
                continue
                
            try:
                selected_event = events[int(event_choice)-1]
                event_id = selected_event[0]
                event = system.create_event(event_id)
                
                if not event:
                    raise EventNotFoundException("Event not found!")
                    
                system.display_event_details(event)
                
                while True:
                    print("\n1. 🎫 Book Tickets")
                    print("2. ❌ Cancel Booking")
                    print("3. ↩ Back to events")
                    action = input("Select option (1-3): ").strip()
                    
                    if action == "3":
                        break
                        
                    elif action == "1":
                        try:
                            num_tickets = int(input("Number of tickets to book: "))
                            if num_tickets <= 0:
                                print("❌ Please enter a positive number!")
                                continue
                                
                            print("\n💰 Ticket Categories:")
                            print("1. 🥈 Silver - ₹200")
                            print("2. 🥇 Gold - ₹500")
                            print("3. 💎 Diamond - ₹1000")
                            category_choice = input("Select ticket category (1-3): ").strip()
                            
                            categories = {1: "Silver", 2: "Gold", 3: "Diamond"}
                            ticket_category = categories.get(int(category_choice)) if category_choice.isdigit() and int(category_choice) in categories else None
                            
                            if not ticket_category:
                                print("❌ Invalid category selection!")
                                continue
                                
                            booking_id = system.book_tickets(event_id, customer_id, num_tickets, ticket_category)
                            
                            if booking_id:
                                print(f"\n✅ Booking successful! Your Booking ID: {booking_id}")
                                print(f"💵 Total cost: ₹{num_tickets * {'Silver':200, 'Gold':500, 'Diamond':1000}[ticket_category]}")
                            else:
                                print("❌ Booking failed!")
                                
                        except ValueError:
                            print("❌ Please enter valid numbers!")
                            
                    elif action == "2":
                        booking_id = input("Enter your Booking ID to cancel: ").strip()
                        try:
                            if system.cancel_booking(booking_id):
                                print("✅ Booking cancelled successfully!")
                            else:
                                print("❌ Cancellation failed!")
                        except InvalidBookingIDException as e:
                            print(f"❌ {e}")
                            
            except (IndexError, ValueError):
                print("❌ Invalid event selection!")
            except EventNotFoundException as e:
                print(f"❌ {e}")

    except Exception as e:
        print(f"❌ An error occurred: {e}")

def main():
    conn = DBConnUtil.get_db_connection()
    if not conn:
        raise NullPointerException("Failed to establish database connection")

    admin = Admin(conn)
    
    try:
        while True:
            display_main_menu()
            choice = input("Enter your choice (1-3): ").strip()
            
            if choice == "1":
                handle_customer_booking(conn)
                
            elif choice == "2":
                print("\n🛠 ADMIN PANEL")
                password = input("Enter admin password: ").strip()
                # In a real system, you would verify the password here
                if password == "admin123":  # Example password
                    admin.create_event()
                else:
                    print("❌ Access denied!")
                    
            elif choice == "3":
                print("\n👋 Thank you for using our Ticket Booking System!")
                break
                
            else:
                print("❌ Invalid choice! Please try again.")
                
    finally:
        conn.close()

if __name__ == "__main__":
    main()