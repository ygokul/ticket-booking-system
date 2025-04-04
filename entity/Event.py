from abc import ABC, abstractmethod


class Event(ABC):
    def __init__(self, event_name, event_date, event_time, venue, total_seats, ticket_price, event_type):
        self._event_name = event_name
        self._event_date = event_date
        self._event_time = event_time
        self._venue = venue
        self._total_seats = total_seats
        self._available_seats = total_seats  # Initially equal to total_seats
        self._ticket_price = ticket_price
        self._event_type = event_type

    @property
    def event_name(self):
        return self._event_name

    @event_name.setter
    def event_name(self, value):
        self._event_name = value

    @property
    def event_date(self):
        return self._event_date

    @event_date.setter
    def event_date(self, value):
        self._event_date = value

    @property
    def event_time(self):
        return self._event_time

    @event_time.setter
    def event_time(self, value):
        self._event_time = value

    @property
    def venue(self):
        return self._venue

    @venue.setter
    def venue(self, value):
        self._venue = value

    @property
    def total_seats(self):
        return self._total_seats

    @total_seats.setter
    def total_seats(self, value):
        self._total_seats = value
        self._available_seats = value  # Optionally reset available seats

    @property
    def available_seats(self):
        return self._available_seats

    @available_seats.setter
    def available_seats(self, value):
        self._available_seats = value

    @property
    def ticket_price(self):
        return self._ticket_price

    @ticket_price.setter
    def ticket_price(self, value):
        self._ticket_price = value

    @property
    def event_type(self):
        return self._event_type

    @event_type.setter
    def event_type(self, value):
        self._event_type = value

    @abstractmethod
    def display_event_info(self):
        """Abstract method to display event type, date, and time"""
        pass
