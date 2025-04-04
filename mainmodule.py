from dao.BookingSystemRepositoryImpl import BookingSystemRepositoryImpl
from entity.Venue import Venue
from entity.Customer import Customer
from entity.Event import Event
from entity.Booking import Booking
from exception.EventNotFoundException import EventNotFoundException
from exception.InvalidBookingIDException import InvalidBookingIDException

class TicketBookingSystem:
    def __init__(self):
        self.repository = BookingSystemRepositoryImpl()
    
class TicketBookingSystem:
    def __init__(self):
        self.repository = BookingSystemRepositoryImpl()
    
    def run(self):
        while True:
            try:
                print("\n            WELCOME TO TICKET BOOKING SYSTEM         ")
                print("1. Create Event")
                print("2. Update Event Details")
                print("3. Book Tickets")
                print("4. Cancel Tickets")
                print("5. Get Available Seats")
                print("6. Get Event Details")
                print("7. Get Booking Details Summary")
                print("8. Get Customer Booking History")
                print("9. List Events by Type")
                print("10. Calculate Event Revenue")
                print("11. Auto-Cancel Unpaid Bookings")
                print("12. Exit")

                choice = int(input("Enter your choice: "))

                if choice == 1:  # Create Event
                    event_name = input("Enter event name: ")
                    date = input("Enter event date (YYYY-MM-DD): ")
                    time = input("Enter event time (HH:MM:SS): ")
                    total_seats = int(input("Enter total seats: "))
                    ticket_price = float(input("Enter ticket price: "))
                    event_type = input("Enter event type (Movie/Sports/Concert): ")
                    venue_name = input("Enter venue name: ")
                    address = input("Enter venue address: ")

                    venue = Venue(venue_name, address)
                    self.repository.create_event(event_name, date, time, total_seats, ticket_price, event_type, venue)

                elif choice == 2:  # Update Event Details
                    event_name = input("Enter event name to update: ")
                    new_date = input("Enter new date (YYYY-MM-DD): ")
                    new_time = input("Enter new time (HH:MM:SS): ")
                    new_ticket_price = float(input("Enter new ticket price: "))

                    self.repository.update_event_details(event_name, new_date, new_time, new_ticket_price)

                elif choice == 3:  # Book Tickets
                    event_name = input("Enter event name: ")
                    num_tickets = int(input("Enter number of tickets: "))
                    customer_name = input("Enter your name: ")

                    self.repository.book_tickets(event_name, num_tickets, customer_name)

                elif choice == 4:  # Cancel Tickets
                    try:
                        booking_id = int(input("Enter booking ID: "))
                        self.repository.cancel_booking(booking_id)
                    except InvalidBookingIDException as e:
                        print(e)

                elif choice == 5:  # Get Available Seats
                    try:
                        event_name = input("Enter event name: ")
                        available_seats = self.repository.get_available_no_of_tickets(event_name)
                        print(f"Available seats for {event_name}: {available_seats}")
                    except EventNotFoundException as e:
                        print(f"⚠️ {e}")
                    except Exception as e:
                        print(f"An error occurred: {e}")

                elif choice == 6:  # Get Event Details
                    try:
                        event_name = input("Enter event name: ")
                        self.repository.get_event_details(event_name)
                    except EventNotFoundException as e:
                        print(f"Error: {e}")

                elif choice == 7:  # Get Booking Details Summary
                    booking_id = int(input("Enter your booking ID: "))
                    self.repository.get_booking_details(booking_id)

                elif choice == 8:  # Get Customer Booking History
                    customer_name = input("Enter customer name: ")
                    self.repository.get_customer_booking_history(customer_name)

                elif choice == 9:  # List Events by Type
                    event_type = input("Enter event type (Movie/Sports/Concert): ")
                    self.repository.list_events_by_type(event_type)

                elif choice == 10:  # Calculate Event Revenue
                    event_name = input("Enter event name: ")
                    revenue = self.repository.calculate_event_revenue(event_name)
                    print(f"Total revenue for {event_name}: ₹{revenue}")

                elif choice == 11:  # Auto-Cancel Unpaid Bookings
                    self.repository.auto_cancel_unpaid_bookings()
                    print("✅ All unpaid bookings have been canceled.")

                elif choice == 12:  # Exit
                    print("Thank you for using the Ticket Booking System!")
                    break

                else:
                    print("❌ Invalid choice! Please enter a number between 1-12.")

            except EventNotFoundException as e:
                print(e)

            except InvalidBookingIDException as e:
                print(e)

            except Exception as e:
                print("⚠️ An error occurred:", e)


if __name__ == "__main__":
    system = TicketBookingSystem()
    system.run()
