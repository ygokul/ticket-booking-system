from abc import ABC, abstractmethod
from entity.event import Event
from entity.venue import Venue
from entity.customer import Customer

class IBookingSystemRepository(ABC):
    @abstractmethod
    def create_event(self, event_name: str, event_date: str, event_time: str, 
                    total_seats: int, ticket_price: float, event_type: str, 
                    venue: Venue, **kwargs) -> Event:
        pass

    @abstractmethod
    def get_event_details(self) -> list[Event]:
        pass

    @abstractmethod
    def get_available_no_of_tickets(self, event_name: str) -> int:
        pass

    @abstractmethod
    def calculate_booking_cost(self, num_tickets: int, event_name: str) -> float:
        pass

    @abstractmethod
    def book_tickets(self, event_name: str, num_tickets: int, customers: list[Customer]) -> bool:
        pass

    @abstractmethod
    def cancel_booking(self, booking_id: int) -> bool:
        pass

    @abstractmethod
    def get_booking_details(self, booking_id: int) -> dict:
        pass