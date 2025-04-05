from datetime import datetime
from entity.customer import Customer
from entity.event import Event

class Booking:
    booking_counter = 1

    def __init__(self, customers: list[Customer], event: Event, num_tickets: int):
        self.booking_id = Booking.booking_counter
        Booking.booking_counter += 1
        self.customers = customers
        self.event = event
        self.num_tickets = num_tickets
        self.total_cost = num_tickets * event.ticket_price
        self.booking_date = datetime.now()

    def display_booking_details(self) -> None:
        print(f"Booking ID: {self.booking_id}")
        print("Customers:")
        for customer in self.customers:
            customer.display_customer_details()
        print("Event Details:")
        self.event.display_event_details()
        print(f"Number of Tickets: {self.num_tickets}")
        print(f"Total Cost: {self.total_cost}")
        print(f"Booking Date: {self.booking_date}")

    def __str__(self) -> str:
        return (f"Booking ID: {self.booking_id}, "
                f"Event: {self.event.event_name}, "
                f"Tickets: {self.num_tickets}, "
                f"Total Cost: {self.total_cost}")