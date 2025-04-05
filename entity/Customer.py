class Customer:
    def __init__(self, customer_name: str, email: str, phone_number: str):
        self.customer_name = customer_name
        self.email = email
        self.phone_number = phone_number

    def display_customer_details(self) -> None:
        print(f"Customer Name: {self.customer_name}")
        print(f"Email: {self.email}")
        print(f"Phone Number: {self.phone_number}")

    def __str__(self) -> str:
        return f"{self.customer_name}, {self.email}, {self.phone_number}"