from dao.booking_service_provider import IBookingSystemServiceProvider
from dao.event_service_provider_impl import EventServiceProviderImpl
from entity.event import Event
from entity.customer import Customer
from entity.booking import Booking
from typing import List
from exception.event_not_found_exception import EventNotFoundException
from exception.invalid_booking_id_exception import InvalidBookingIDException

class BookingSystemServiceProviderImpl(EventServiceProviderImpl, IBookingSystemServiceProvider):
    def __init__(self):
        super().__init__()
        self.bookings: List[Booking] = []

    def calculate_booking_cost(self, num_tickets: int, event: Event) -> float:
        return num_tickets * event.ticket_price

    def book_tickets(self, event_name: str, num_tickets: int, customers: List[Customer]) -> bool:
        event = None
        for e in self.events:
            if e.event_name == event_name:
                event = e
                break
        
        if not event:
            raise EventNotFoundException(f"Event '{event_name}' not found")
        
        if event.available_seats < num_tickets:
            return False
        
        if len(customers) != num_tickets:
            return False
        
        event.book_tickets(num_tickets)
        booking = Booking(customers, event, num_tickets)
        self.bookings.append(booking)
        return True

    def cancel_booking(self, booking_id: int) -> bool:
        booking = None
        for b in self.bookings:
            if b.booking_id == booking_id:
                booking = b
                break
        
        if not booking:
            raise InvalidBookingIDException(f"Booking ID {booking_id} not found")
        
        booking.event.cancel_booking(booking.num_tickets)
        self.bookings.remove(booking)
        return True

    def get_booking_details(self, booking_id: int) -> dict:
        for booking in self.bookings:
            if booking.booking_id == booking_id:
                return {
                    'booking_id': booking.booking_id,
                    'event_name': booking.event.event_name,
                    'num_tickets': booking.num_tickets,
                    'total_cost': booking.total_cost,
                    'booking_date': booking.booking_date,
                    'customers': [str(customer) for customer in booking.customers]
                }
        raise InvalidBookingIDException(f"Booking ID {booking_id} not found")
    
    def book_tickets(self, event_name: str, num_tickets: int, customers: List[Customer], ticket_category: str) -> bool:
        event = None
        for e in self.events:
            if e.event_name == event_name:
                event = e
                break
        
        if not event:
            raise EventNotFoundException(f"Event '{event_name}' not found")
        
        try:
            total_cost = event.calculate_ticket_cost(ticket_category, num_tickets)
        except ValueError as e:
            print(f"Error: {e}")
            return False
        
        if event.available_seats < num_tickets:
            print(f"Tickets unavailable. Only {event.available_seats} tickets remaining.")
            return False
        
        if len(customers) != num_tickets:
            return False
        
        event.book_tickets(num_tickets)
        booking = Booking(customers, event, num_tickets, total_cost)
        self.bookings.append(booking)
        print(f"Booking successful! Total cost: ₹{total_cost:.2f}")
        return True