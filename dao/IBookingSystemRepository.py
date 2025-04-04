from abc import ABC, abstractmethod

class IBookingSystemRepository(ABC):
    @abstractmethod
    def create_event(self, event_name, date, time, total_seats, ticket_price, event_type, venue):
        pass

    @abstractmethod
    def getEventDetails(self):
        pass

    @abstractmethod
    def getAvailableNoOfTickets(self):
        pass

    @abstractmethod
    def calculate_booking_cost(self, num_tickets, ticket_price):
        pass

    @abstractmethod
    def book_tickets(self, eventname, num_tickets):
        pass

    @abstractmethod
    def cancel_booking(self, booking_id):
        pass

    @abstractmethod
    def get_booking_details(self, booking_id):
        pass

    @abstractmethod
    def get_customer_with_max_tickets(self):
        pass