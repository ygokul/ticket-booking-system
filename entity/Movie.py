from entity.Event import Event

class Movie(Event):
    def __init__(self, event_name, event_date, event_time, venue, total_seats, ticket_price, genre, actor_name, actress_name):
        super().__init__(event_name, event_date, event_time, venue, total_seats, ticket_price, "Movie")
        self.genre = genre
        self.actor_name = actor_name
        self.actress_name = actress_name
    
    def display_event_info(self):
        print(f"Event Type: {self.event_type}")
        print(f"Event Date: {self.event_date}")
        print(f"Event Time: {self.event_time}")
