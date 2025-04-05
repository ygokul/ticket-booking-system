class Venue:
    def __init__(self, venue_name: str, address: str):
        self.venue_name = venue_name
        self.address = address

    def display_venue_details(self) -> None:
        print(f"Venue Name: {self.venue_name}")
        print(f"Address: {self.address}")

    def __str__(self) -> str:
        return f"{self.venue_name}, {self.address}"