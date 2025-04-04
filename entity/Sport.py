from entity.Event import Event

class Sport(Event):
    def __init__(self, event_name, event_date, event_time, venue, total_seats, ticket_price, sport_name, teams_name):
        super().__init__(event_name, event_date, event_time, venue, total_seats, ticket_price, "Sport")
        self.sport_name = sport_name
        self.teams_name = teams_name

     def display_event_info(self):
        print(f"Event Type: {self.event_type}")
        print(f"Event Date: {self.event_date}")
        print(f"Event Time: {self.event_time}") 
