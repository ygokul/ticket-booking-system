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
    
    def run(self):
        while True:
            try:
                print("            WELCOME TO TICKET BOOKING SYSTEM         ")
                print("1. Create Event")
                print("2. Book Tickets")
                print("3. Cancel Tickets")
                print("4. Get Available Seats")
                print("5. Get Event Details")
                print("6. Get Booking Details Summary")
                print("7. Customer Booked maximum Tickets")
                print("8. Exit")
                
                choice = int(input("Enter your choice: "))
                
                if choice == 1:
                    event_name = input("Enter event name: ")
                    date = input("Enter event date (YYYY-MM-DD): ")
                    time = input("Enter event time (HH:MM:SS): ")
                    total_seats = int(input("Enter total seats: "))
                    ticket_price = float(input("Enter ticket price: "))
                    event_type = input("Enter event type (Movie/Sports/Concert): ")
                    venue_name = input("Enter venue name: ")
                    address = input("Enter venue address: ")
                    
                    venue = Venue(venue_name, address)  # Create a Venue object
                    self.repository.create_event(event_name, date, time, total_seats, ticket_price, event_type, venue)

                    

                elif choice == 2:
                    eventname = input("Enter event name: ")
                    num_tickets = int(input("Enter number of tickets: "))
                    
                    # Directly call book_tickets without customers
                    self.repository.book_tickets(eventname, num_tickets)

                elif choice == 3:
                    try:
                        booking_id = int(input("Enter booking ID: "))
                        self.repository.cancel_booking(booking_id)
                    except InvalidBookingIDException as e:
                        print(e)

                elif choice == 4:
                    try:
                        self.repository.getAvailableNoOfTickets()
                    except EventNotFoundException as e:
                        print(f"⚠️ {e}")
                    except Exception as e:
                        print(f"An error occurred: {e}")

                
                elif choice == 5:
                    try:
                        self.repository.getEventDetails()
                    except EventNotFoundException as e:
                        print(f"Error: {e}")

                elif choice == 6:
                    booking_id = int(input("Enter your booking ID: "))
                    self.repository.get_booking_details(booking_id)
                
                elif choice == 7:
                    self.repository.get_customer_with_max_tickets()

                elif choice == 8:
                    break
                
                else:
                    print("Invalid choice!")
            
            except EventNotFoundException as e:
                print(e)
            
            except InvalidBookingIDException as e:
                print(e)
            
            except Exception as e:
                print("An error occurred:", e)

if __name__ == "__main__":
    system = TicketBookingSystem()
    system.run()