class Customer:
    def __init__(self, customer_name="", email="", phone_number=""):
        self._customer_name = customer_name
        self._email = email
        self._phone_number = phone_number

    @property
    def customer_name(self):
        return self._customer_name

    @customer_name.setter
    def customer_name(self, value):
        self._customer_name = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        self._email = value

    @property
    def phone_number(self):
        return self._phone_number

    @phone_number.setter
    def phone_number(self, value):
        self._phone_number = value
