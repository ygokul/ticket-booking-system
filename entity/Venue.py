class Venue:
    def __init__(self, venue_name="", address=""):
        self._venue_name = venue_name
        self._address = address

    # Getter for venue_name
    @property
    def venue_name(self):
        return self._venue_name

    # Setter for venue_name
    @venue_name.setter
    def venue_name(self, value):
        self._venue_name = value

    # Getter for address
    @property
    def address(self):
        return self._address

    # Setter for address
    @address.setter
    def address(self, value):
        self._address = value

    def display_venue_details(self):
        print(f"Venue: {self.venue_name}, Address: {self.address}")
