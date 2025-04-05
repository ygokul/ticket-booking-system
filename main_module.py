from dao.booking_service_provider_impl import BookingSystemServiceProviderImpl
from entity.venue import Venue
from entity.customer import Customer
from exception.event_not_found_exception import EventNotFoundException
from exception.invalid_booking_id_exception import InvalidBookingIDException

def main():
    booking_system = BookingSystemServiceProviderImpl()
    
    # Create some venues
    venue1 = Venue("Grand Theater", "123 Main St, New York")
    venue2 = Venue("Sports Arena", "456 Oak Ave, Los Angeles")
    venue3 = Venue("Concert Hall", "789 Pine Rd, Chicago")
    
    # Create some events
    try:
        booking_system.create_event(
            "Avengers Premiere", "2023-12-15", "18:00:00", 
            200, 1200.00, "Movie", venue1,
            genre="Action", actor_name="Robert Downey Jr.", actress_name="Scarlett Johansson"
        )
        
        booking_system.create_event(
            "World Cup Final", "2023-12-18", "15:00:00", 
            50000, 2500.00, "Sports", venue2,
            sport_name="Football", teams_name="Argentina vs France"
        )
        
        booking_system.create_event(
            "Coldplay Concert", "2023-12-20", "20:00:00", 
            10000, 3500.00, "Concert", venue3,
            artist="Coldplay", concert_type="Rock"
        )
    except ValueError as e:
        print(f"Error creating event: {e}")
        return
    
    # Menu-driven interface
    while True:
        print("\nTicket Booking System")
        print("1. Display all events")
        print("2. Book tickets")
        print("3. Cancel booking")
        print("4. View booking details")
        print("5. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            print("\nAvailable Events:")
            events = booking_system.get_event_details()
            for i, event in enumerate(events, 1):
                print(f"{i}. {event.event_name} ({event.event_type}) - Available seats: {event.available_seats}")
        
        elif choice == "2":
            event_name = input("Enter event name: ")
            try:
                num_tickets = int(input("Enter number of tickets: "))
                if num_tickets <= 0:
                    print("Number of tickets must be positive")
                    continue
                
                customers = []
                for i in range(num_tickets):
                    print(f"\nEnter details for ticket {i+1}:")
                    name = input("Customer name: ")
                    email = input("Email: ")
                    phone = input("Phone number: ")
                    customers.append(Customer(name, email, phone))
                
                if booking_system.book_tickets(event_name, num_tickets, customers):
                    print(f"Successfully booked {num_tickets} tickets for {event_name}")
                else:
                    print("Failed to book tickets. Not enough seats available.")
            
            except ValueError:
                print("Invalid input. Please enter a valid number.")
            except EventNotFoundException as e:
                print(f"Error: {e}")
        
        elif choice == "3":
            try:
                booking_id = int(input("Enter booking ID to cancel: "))
                if booking_system.cancel_booking(booking_id):
                    print(f"Booking {booking_id} cancelled successfully")
                else:
                    print("Failed to cancel booking")
            except ValueError:
                print("Invalid input. Please enter a valid booking ID.")
            except InvalidBookingIDException as e:
                print(f"Error: {e}")
        
        elif choice == "4":
            try:
                booking_id = int(input("Enter booking ID to view details: "))
                details = booking_system.get_booking_details(booking_id)
                print("\nBooking Details:")
                print(f"Booking ID: {details['booking_id']}")
                print(f"Event: {details['event_name']}")
                print(f"Number of Tickets: {details['num_tickets']}")
                print(f"Total Cost: {details['total_cost']}")
                print(f"Booking Date: {details['booking_date']}")
                print("Customers:")
                for customer in details['customers']:
                    print(f" - {customer}")
            except ValueError:
                print("Invalid input. Please enter a valid booking ID.")
            except InvalidBookingIDException as e:
                print(f"Error: {e}")
        
        elif choice == "5":
            print("Exiting the system. Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()