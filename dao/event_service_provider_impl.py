from dao.event_service_provider import IEventServiceProvider
from entity.event import Event, Movie, Concert, Sports
from entity.venue import Venue
from typing import List

class EventServiceProviderImpl(IEventServiceProvider):
    def __init__(self):
        self.events: List[Event] = []

    def create_event(self, event_name: str, event_date: str, event_time: str, 
                    total_seats: int, ticket_price: float, event_type: str, 
                    venue: Venue, **kwargs) -> Event:
        if event_type == "Movie":
            event = Movie(event_name, event_date, event_time, venue, total_seats, 
                         ticket_price, kwargs['genre'], kwargs['actor_name'], kwargs['actress_name'])
        elif event_type == "Concert":
            event = Concert(event_name, event_date, event_time, venue, total_seats, 
                           ticket_price, kwargs['artist'], kwargs['concert_type'])
        elif event_type == "Sports":
            event = Sports(event_name, event_date, event_time, venue, total_seats, 
                          ticket_price, kwargs['sport_name'], kwargs['teams_name'])
        else:
            raise ValueError("Invalid event type")
        
        self.events.append(event)
        return event

    def get_event_details(self) -> List[Event]:
        return self.events

    def get_available_no_of_tickets(self, event_name: str) -> int:
        for event in self.events:
            if event.event_name == event_name:
                return event.available_seats
        return 0