from util.db_connection import DBConnUtil
from dao.bean.TicketBookingSystem import TicketBookingSystem
from dao.Admin import Admin
from exception.EventNotFoundException import EventNotFoundException
from exception.InvalidBookingIDException import InvalidBookingIDException
from exception.NullPointerException import NullPointerException

def book_tickets():
    conn = DBConnUtil.get_db_connection()
    if not conn:
        raise NullPointerException("Failed to establish database connection")

    system = TicketBookingSystem(conn)

    try:
        print("\n🔹 Welcome to the Ticket Booking System 🔹")
        # role = input("Are you an Admin or a Customer? (Admin/Customer/Exit): ").strip().lower()

        # if role == "customer":
            # Customer registration/login
        with conn.cursor() as cursor:
            email = input("Enter your email: ").strip()
            cursor.execute("SELECT customer_id FROM Customer WHERE email = %s", (email,))
            result = cursor.fetchone()

            if result:
                customer_id = result[0]
                print(f"✅ Welcome back!")
            else:
                print("❌ No user exists!")
                print("📝 Please register to continue.")
                customer_name = input("Enter your name: ").strip()
                phone_number = input("Enter your phone number: ").strip()
                cursor.execute("""
                    INSERT INTO Customer (customer_name, email, phone_number)
                    VALUES (%s, %s, %s)
                """, (customer_name, email, phone_number))
                conn.commit()
                customer_id = cursor.lastrowid
                print("✅ Registration successful!")

        event_type = input("Which event do you want to book? (Movie/Concert/Sports): ").strip().capitalize()

        if event_type not in ["Movie", "Concert", "Sports"]:
            print("❌ Invalid event type! Please enter 'Movie', 'Concert', or 'Sports'.")
            return

        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT event_id, event_name, event_date, event_time 
                FROM Event 
                WHERE event_type = %s
            """, (event_type,))
            events = cursor.fetchall()

        if not events:
            print(f"❌ No {event_type} events available for booking!")
            return

        print(f"\n🎟 Available {event_type} Events:")
        for event in events:
            print(f"🔹 {event[0]}. {event[1]} on {event[2]} at {event[3]}")

        event_id = int(input("\nEnter Event ID to proceed with booking: "))
        try:
            event = system.create_event(event_id)
            if event is None or event.event_name is None:
                raise EventNotFoundException("Invalid Event ID! Please select from the available events.")
            
            system.display_event_details(event)

            while True:
                action = input("Type 'Book' to book tickets, 'Cancel' to cancel a booking, or 'Exit' to quit: ").strip().lower()
                if action == "exit":
                    print("✅ Exiting the booking system. Thank you!")
                    break

                elif action == "book":
                    num_tickets = int(input("Enter the number of tickets to book: "))
                    print("💰 Ticket Prices:")
                    print("   🥈 Silver  - ₹200")
                    print("   🥇 Gold    - ₹500")
                    print("   💎 Diamond - ₹1000")
                    print("ℹ️  Final price depends on the selected category.")
                    ticket_category = input("Enter the ticket category (Silver/Gold/Diamond): ").strip().capitalize()
                    booking_id = system.book_tickets(event_id, customer_id, num_tickets, ticket_category)
                    
                    if booking_id:
                        print(f"✅ Tickets booked successfully for {event.event_name}!")
                        print(f"📄 Your Booking ID: {booking_id}")
                    else:
                        print("❌ Booking failed! Please try again.")

                elif action == "cancel":
                    booking_id = int(input("Enter Booking ID to cancel: "))
                    try:
                        system.cancel_booking(booking_id)
                        print("✅ Booking cancelled successfully!")
                    except InvalidBookingIDException as e:
                        print(f"❌ {e}")

        except EventNotFoundException as e:
            print(f"❌ {e}")

    finally:
        conn.close()

if __name__ == "__main__":
    book_tickets()