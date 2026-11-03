from dataclasses import dataclass, field



@dataclass
class Customer:
    customer_id : str
    name : str
    phone_number : str
    national_id : int 
    driving_licence : str 
    rentals : list["Rental"] = field(default_factory=list)

    def __post_init__(self):
        if not self.driving_licence:
            raise ValueError("Driving license is Mandatory!")

    def add_rental(self, rental):
        self.rentals.append(rental)

    def display_details(self):
        return f"{self.name} (ID: {self.customer_id})"

    def view_rental_history(self):
        return self.rentals
