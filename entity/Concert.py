from entity.Event import Event

class Concert(Event):
    def __init__(self, event_name, event_date, event_time, venue, total_seats, ticket_price, artist, concert_type):
        super().__init__(event_name, event_date, event_time, venue, total_seats, ticket_price, "Concert")
        self.artist = artist
        self.concert_type = concert_type
    
    def display_event_info(self):
        print(f"Event Type: {self.event_type}")
        print(f"Event Date: {self.event_date}")
        print(f"Event Time: {self.event_time}")
