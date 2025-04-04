class Booking:
    booking_counter = 1

    def __init__(self, customers, event, num_tickets):
        self._bookingId = Booking.booking_counter
        Booking.booking_counter += 1
        self._customers = customers
        self._event = event
        self._num_tickets = num_tickets
        self._total_cost = event.ticket_price * num_tickets

    @property
    def bookingId(self):
        return self._bookingId

    @property
    def customers(self):
        return self._customers

    @customers.setter
    def customers(self, value):
        self._customers = value

    @property
    def event(self):
        return self._event

    @event.setter
    def event(self, value):
        self._event = value
        self._total_cost = value.ticket_price * self._num_tickets  # Update cost if event changes

    @property
    def num_tickets(self):
        return self._num_tickets

    @num_tickets.setter
    def num_tickets(self, value):
        self._num_tickets = value
        self._total_cost = self._event.ticket_price * value  # Update total cost on ticket change

    @property
    def total_cost(self):
        return self._total_cost
