import mysql.connector
from dao.IBookingSystemRepository import IBookingSystemRepository
from util.DBUtil import DBUtil
from exception.EventNotFoundException import EventNotFoundException
from exception.InvalidBookingIDException import InvalidBookingIDException
from tabulate import tabulate

class BookingSystemRepositoryImpl(IBookingSystemRepository):
    def __init__(self):
        self.conn = DBUtil.getDBConn()
        self.cursor = self.conn.cursor()
    
    def create_event(self, event_name, date, time, total_seats, ticket_price, event_type, venue):
        sql = """INSERT INTO event (event_name, event_date, event_time, total_seats, available_seats, ticket_price, event_type, venue_name)  
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""

        values = (event_name, date, time, total_seats, total_seats, ticket_price, event_type, venue.venue_name)

        try:
            self.cursor.execute(sql, values)
            self.conn.commit()
            print(f"Event '{event_name}' created successfully at venue '{venue.venue_name}'!")  

            # Fetch and display the newly inserted row
            self.cursor.execute("SELECT * FROM event WHERE event_name = %s AND event_date = %s AND event_time = %s", 
                                (event_name, date, time))
            new_event = self.cursor.fetchall()

            print("\n🔹 Added Event Details:")
            for row in new_event:
                print(row)

        except Exception as e:
            print("Error creating event:", e)


   

    def getEventDetails(self):
        self.cursor.execute("SELECT * FROM event")
        events = self.cursor.fetchall()
        
        if not events:
            raise EventNotFoundException("No events found in the system.")
        
        for event in events:
            print(event)



    def getAvailableNoOfTickets(self):
        try:
            self.cursor.execute("SELECT event_name, available_seats FROM event")
            events = self.cursor.fetchall()
            
            if not events:
                raise EventNotFoundException("No events found in the system.")

            # Catchy message
            print("\n🎉 These are the available limited offers! Grab your tickets before they're gone! 🎟️🔥\n")

            # Convert data to a table format
            table = tabulate(events, headers=["Event Name", "Available Tickets"], tablefmt="fancy_grid")

            print(table)

        except EventNotFoundException as e:
            print(f"⚠️ {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    
    def calculate_booking_cost(self, num_tickets, ticket_price):
        return num_tickets * ticket_price
    
    def book_tickets(self, eventname, num_tickets):
        try:
            # Fetch available seats & ticket price
            self.cursor.execute(
                "SELECT available_seats, ticket_price FROM event WHERE event_name = %s", 
                (eventname,)
            )
            events = self.cursor.fetchone()

            if not events:
                raise EventNotFoundException("Event not found!")

            available_seats, ticket_price = events

            if available_seats >= num_tickets:
                total_cost = self.calculate_booking_cost(num_tickets, ticket_price)

                # Update available seats (no tracking in bookings table)
                self.cursor.execute(
                    "UPDATE event SET available_seats = available_seats - %s WHERE event_name = %s", 
                    (num_tickets, eventname)
                )

                self.conn.commit()

                # Fetch updated available seats
                self.cursor.execute("SELECT available_seats FROM event WHERE event_name = %s", (eventname,))
                updated = self.cursor.fetchone()

                # ✅ Final output
                print(f"\n✅ Tickets booked successfully for event: {eventname}")
                print(f"🎟️ Tickets Booked: {num_tickets}")
                print(f"💰 Total Cost: ₹{total_cost:.2f}")
                print(f"🪑 Available Seats Left: {updated[0]}")
                print("⚠️ Hurry up! Only a few seats left!")

            else:
                print("❌ Not enough available seats!")

        except Exception as e:
            print("❌ Error booking tickets:", e)

    def cancel_booking(self, booking_id):
        # Step 1: Get event_name and num_tickets from booking
        self.cursor.execute("SELECT event_name, num_tickets FROM booking WHERE booking_id = %s", (booking_id,))
        booking = self.cursor.fetchone()
        if not booking:
            raise InvalidBookingIDException("Invalid booking ID!")

        event_name, num_tickets = booking

        # Step 2: Get ticket price from events table
        self.cursor.execute("SELECT ticket_price FROM event WHERE event_name = %s", (event_name,))
        event = self.cursor.fetchone()
        if not event:
            raise Exception("Event not found for the booking!")  # just in case

        ticket_price = event[0]

        # Step 3: Calculate refund
        refund_amount = self.calculate_booking_cost(num_tickets, ticket_price)

        # Step 4: Update available seats
        self.cursor.execute(
            "UPDATE event SET available_seats = available_seats + %s WHERE event_name = %s",
            (num_tickets, event_name)
        )

        # Step 5: Delete booking
        self.cursor.execute("DELETE FROM booking WHERE booking_id = %s", (booking_id,))
        self.conn.commit()

        # Step 6: Show success and refund
        print("Booking cancelled successfully!")
        print(f"Refund Amount: ₹{refund_amount:.2f}")

    def get_booking_details(self, booking_id):
        self.cursor.execute("SELECT * FROM booking WHERE booking_id = %s", (booking_id,))
        booking = self.cursor.fetchone()
        
        if booking:
            headers = ["Booking ID", "No. of Tickets", "Total Cost", "Booking Date", "Event Name"]
            
            # Sentence format summary
            print("\n📄 Booking Summary:")
            print(f"Booking ID {booking[0]} is for event '{booking[4]}' on {booking[3]}.")
            print(f"Number of tickets: {booking[1]}, Total cost: ₹{booking[2]:.2f}.\n")
            
            # Tabular format
            print("📊 Booking Details:")
            print(tabulate([booking], headers=headers, tablefmt="fancy_grid"))
        else:
            print("No booking found with the given ID.")

    def get_customer_with_max_tickets(self):
        query = """
            SELECT c.customer_name, c.phone_number, b.num_tickets
            FROM customer c
            JOIN booking b ON c.BOOKING_ID = b.booking_id
            ORDER BY b.num_tickets DESC
            LIMIT 1
        """
        self.cursor.execute(query)
        result = self.cursor.fetchone()

        if result:
            print("\n📢 Customer with the Highest Ticket Booking:\n")
            print(f"👤 Name         : {result[0]}")
            print(f"📞 Phone Number : {result[1]}")
            print(f"🎟️ Tickets Booked: {result[2]}")
        else:
            print("No bookings found.")


