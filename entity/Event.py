from abc import ABC, abstractmethod
from datetime import datetime
from entity.venue import Venue

class Event(ABC):
    def __init__(self, event_name: str, event_date: str, event_time: str, venue: Venue, 
                 total_seats: int, ticket_price: float, event_type: str):
        self.event_name = event_name
        self.event_date = datetime.strptime(event_date, "%Y-%m-%d").date()
        self.event_time = datetime.strptime(event_time, "%H:%M:%S").time()
        self.venue = venue
        self.total_seats = total_seats
        self.available_seats = total_seats
        self.ticket_price = ticket_price
        self.event_type = event_type

    def calculate_total_revenue(self) -> float:
        return (self.total_seats - self.available_seats) * self.ticket_price

    def get_booked_no_of_tickets(self) -> int:
        return self.total_seats - self.available_seats

    def book_tickets(self, num_tickets: int) -> bool:
        if self.available_seats >= num_tickets:
            self.available_seats -= num_tickets
            return True
        return False

    def cancel_booking(self, num_tickets: int) -> None:
        self.available_seats += num_tickets
        if self.available_seats > self.total_seats:
            self.available_seats = self.total_seats

    @abstractmethod
    def display_event_details(self) -> None:
        pass

    def __str__(self) -> str:
        return (f"Event Name: {self.event_name}\n"
                f"Date: {self.event_date}\n"
                f"Time: {self.event_time}\n"
                f"Venue: {self.venue.venue_name}\n"
                f"Total Seats: {self.total_seats}\n"
                f"Available Seats: {self.available_seats}\n"
                f"Ticket Price: {self.ticket_price}\n"
                f"Event Type: {self.event_type}")


class Movie(Event):
    def __init__(self, event_name: str, event_date: str, event_time: str, venue: Venue, 
                 total_seats: int, ticket_price: float, genre: str, actor_name: str, actress_name: str):
        super().__init__(event_name, event_date, event_time, venue, total_seats, ticket_price, "Movie")
        self.genre = genre
        self.actor_name = actor_name
        self.actress_name = actress_name

    def display_event_details(self) -> None:
        print(super().__str__())
        print(f"Genre: {self.genre}")
        print(f"Actor: {self.actor_name}")
        print(f"Actress: {self.actress_name}")


class Concert(Event):
    def __init__(self, event_name: str, event_date: str, event_time: str, venue: Venue, 
                 total_seats: int, ticket_price: float, artist: str, concert_type: str):
        super().__init__(event_name, event_date, event_time, venue, total_seats, ticket_price, "Concert")
        self.artist = artist
        self.concert_type = concert_type

    def display_event_details(self) -> None:
        print(super().__str__())
        print(f"Artist: {self.artist}")
        print(f"Concert Type: {self.concert_type}")


class Sports(Event):
    def __init__(self, event_name: str, event_date: str, event_time: str, venue: Venue, 
                 total_seats: int, ticket_price: float, sport_name: str, teams_name: str):
        super().__init__(event_name, event_date, event_time, venue, total_seats, ticket_price, "Sports")
        self.sport_name = sport_name
        self.teams_name = teams_name

    def display_event_details(self) -> None:
        print(super().__str__())
        print(f"Sport: {self.sport_name}")
        print(f"Teams: {self.teams_name}")