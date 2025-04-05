from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, Optional
from entity.venue import Venue

class Event(ABC):
    def __init__(self, event_name: str = "", event_date: str = "", event_time: str = "", 
                venue: Optional[Venue] = None, total_seats: int = 0, 
                ticket_price: float = 0.0, event_type: str = ""):
        """Default constructor with optional parameters for overloading"""
        self._event_name = event_name
        self._event_date = datetime.strptime(event_date, "%Y-%m-%d").date() if event_date else None
        self._event_time = datetime.strptime(event_time, "%H:%M:%S").time() if event_time else None
        self._venue = venue
        self._total_seats = total_seats
        self._available_seats = total_seats
        self._ticket_price = ticket_price
        self._event_type = event_type
        self.ticket_categories: Dict[str, float] = {
            'Silver': 1.0,
            'Gold': 1.5,
            'Diamond': 2.0
        }

    # Property getters and setters
    @property
    def event_name(self) -> str:
        return self._event_name

    @event_name.setter
    def event_name(self, value: str) -> None:
        self._event_name = value

    @property
    def event_date(self):
        return self._event_date

    @event_date.setter
    def event_date(self, value: str) -> None:
        self._event_date = datetime.strptime(value, "%Y-%m-%d").date()

    @property
    def event_time(self):
        return self._event_time

    @event_time.setter
    def event_time(self, value: str) -> None:
        self._event_time = datetime.strptime(value, "%H:%M:%S").time()

    @property
    def venue(self) -> Optional[Venue]:
        return self._venue

    @venue.setter
    def venue(self, value: Optional[Venue]) -> None:
        self._venue = value

    @property
    def total_seats(self) -> int:
        return self._total_seats

    @total_seats.setter
    def total_seats(self, value: int) -> None:
        self._total_seats = value
        self._available_seats = value

    @property
    def available_seats(self) -> int:
        return self._available_seats
    
    @available_seats.setter
    def available_seats(self, value: int) -> None:
        if value < 0:
            raise ValueError("Available seats cannot be negative")
        if value > self._total_seats:
            raise ValueError("Available seats cannot exceed total seats")
        self._available_seats = value

    @property
    def ticket_price(self) -> float:
        return self._ticket_price

    @ticket_price.setter
    def ticket_price(self, value: float) -> None:
        if value < 0:
            raise ValueError("Ticket price cannot be negative")
        self._ticket_price = value

    @property
    def event_type(self) -> str:
        return self._event_type

    @event_type.setter
    def event_type(self, value: str) -> None:
        self._event_type = value

    @property
    def base_ticket_price(self) -> float:
        return self._ticket_price

    # Business logic methods
    def calculate_ticket_cost(self, category: str, num_tickets: int) -> float:
        """Calculate total cost for tickets in a specific category"""
        if category not in self.ticket_categories:
            raise ValueError(f"Invalid ticket category: {category}")
        if num_tickets <= 0:
            raise ValueError("Number of tickets must be positive")
        return self.base_ticket_price * self.ticket_categories[category] * num_tickets

    def calculate_total_revenue(self) -> float:
        """Calculate total revenue from tickets sold"""
        return (self.total_seats - self.available_seats) * self.ticket_price

    def get_booked_no_of_tickets(self) -> int:
        """Get number of tickets already booked"""
        return self.total_seats - self.available_seats

    def book_tickets(self, num_tickets: int) -> bool:
        """Book specified number of tickets if available"""
        if num_tickets <= 0:
            raise ValueError("Number of tickets must be positive")
        if self.available_seats >= num_tickets:
            self.available_seats -= num_tickets
            return True
        return False

    def cancel_booking(self, num_tickets: int) -> None:
        """Cancel booking and make seats available again"""
        if num_tickets <= 0:
            raise ValueError("Number of tickets must be positive")
        self.available_seats += num_tickets

    @abstractmethod
    def display_event_details(self) -> None:
        """Abstract method to display event details"""
        pass

    def __str__(self) -> str:
        """String representation of the event"""
        venue_name = self.venue.venue_name if self.venue else "No venue assigned"
        return (f"Event Name: {self.event_name}\n"
                f"Date: {self.event_date}\n"
                f"Time: {self.event_time}\n"
                f"Venue: {venue_name}\n"
                f"Total Seats: {self.total_seats}\n"
                f"Available Seats: {self.available_seats}\n"
                f"Ticket Price: {self.ticket_price}\n"
                f"Event Type: {self.event_type}")


class Movie(Event):
    def __init__(self, event_name: str, event_date: str, event_time: str, venue: Venue, 
                 total_seats: int, ticket_price: float, genre: str, actor_name: str, actress_name: str):
        super().__init__(event_name, event_date, event_time, venue, total_seats, ticket_price, "Movie")
        self._genre = genre
        self._actor_name = actor_name
        self._actress_name = actress_name

    @property
    def genre(self) -> str:
        return self._genre

    @genre.setter
    def genre(self, value: str) -> None:
        self._genre = value

    @property
    def actor_name(self) -> str:
        return self._actor_name

    @actor_name.setter
    def actor_name(self, value: str) -> None:
        self._actor_name = value

    @property
    def actress_name(self) -> str:
        return self._actress_name

    @actress_name.setter
    def actress_name(self, value: str) -> None:
        self._actress_name = value

    def display_event_details(self) -> None:
        """Display all movie-specific details"""
        print(super().__str__())
        print(f"Genre: {self.genre}")
        print(f"Actor: {self.actor_name}")
        print(f"Actress: {self.actress_name}")


class Concert(Event):
    def __init__(self, event_name: str, event_date: str, event_time: str, venue: Venue, 
                 total_seats: int, ticket_price: float, artist: str, concert_type: str):
        super().__init__(event_name, event_date, event_time, venue, total_seats, ticket_price, "Concert")
        self._artist = artist
        self._concert_type = concert_type

    @property
    def artist(self) -> str:
        return self._artist

    @artist.setter
    def artist(self, value: str) -> None:
        self._artist = value

    @property
    def concert_type(self) -> str:
        return self._concert_type

    @concert_type.setter
    def concert_type(self, value: str) -> None:
        self._concert_type = value

    def display_event_details(self) -> None:
        """Display all concert-specific details"""
        print(super().__str__())
        print(f"Artist: {self.artist}")
        print(f"Concert Type: {self.concert_type}")


class Sports(Event):
    def __init__(self, event_name: str, event_date: str, event_time: str, venue: Venue, 
                 total_seats: int, ticket_price: float, sport_name: str, teams_name: str):
        super().__init__(event_name, event_date, event_time, venue, total_seats, ticket_price, "Sports")
        self._sport_name = sport_name
        self._teams_name = teams_name

    @property
    def sport_name(self) -> str:
        return self._sport_name

    @sport_name.setter
    def sport_name(self, value: str) -> None:
        self._sport_name = value

    @property
    def teams_name(self) -> str:
        return self._teams_name

    @teams_name.setter
    def teams_name(self, value: str) -> None:
        self._teams_name = value

    def display_event_details(self) -> None:
        """Display all sports-specific details"""
        print(super().__str__())
        print(f"Sport: {self.sport_name}")
        print(f"Teams: {self.teams_name}")