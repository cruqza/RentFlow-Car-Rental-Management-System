from dataclasses import dataclass, field
from datetime import date
from vehicle import Vehicle
from customer import Customer
from enum import Enum


class RentalStatus(Enum):
    ACTIVE = "active"
    CLOSED = "closed"

@dataclass
class Rental:
    rental_id : str 
    customer : Customer 
    vehicle : Vehicle
    rental_days : int 
    start_date : date = field(default_factory=date.today)
    actual_days : int = 0
    status : RentalStatus = RentalStatus.ACTIVE
    base_cost : float = 0.0
    late_fee : float = 0.0
    damage_control : float = 0.0
    __paid : bool = False


    def __post_init__(self):
        if self.rental_days <= 0:
            raise ValueError(" Rental days must be atleast 1 day.")
        if not self.vehicle.is_available():
            raise ValueError(f"{self.vehicle.make} {self.vehicle.model} is not available.")
        self.base_cost = self.vehicle.rental_cost(self.rental_days)
        self.vehicle.mark_as_rented()
        self.customer.add_rental(self)


    def calculate_late_fee(self) -> float:
        if self.actual_days > self.rental_days:
            extra_days = self.actual_days - self.rental_days
            return extra_days * self.vehicle.daily_rate * 1.2  #apply 20% penalty
        return 0.0

    def calculate_total(self) -> float:
        return self.base_cost + self.late_fee + self.damage_control


    def complete_rental(self, actual_days : int, damage_control : float = 0.0):
        self.actual_days = actual_days
        self.damage_control = max(0.0, damage_control)

        self.late_fee = self.calculate_late_fee()

        self.status = RentalStatus.CLOSED
        self.vehicle.mark_as_available()


    def mark_as_paid(self):
        self.__paid = True

    def is_paid(self) -> bool:
        return self.__paid

    def display_rental_details(self):
        state = "ACTIVE" if self.status == RentalStatus.ACTIVE else 'CLOSED'
        paid  = "PAID" if self.is_paid() else "UNPAID"
        print(f"[{state} | {paid}] {self.rental_id}: "f" Customer Name : {self.customer.name} | Phone Number : {self.customer.phone_number} | Licence : {self.customer.driving_licence} | Vehichle : {self.vehicle.make} {self.vehicle.model} | "
              f"booked {self.rental_days}d, actual {self.actual_days}d | "
              f"base={self.base_cost}, late={self.late_fee}, damage={self.damage_control} | "
              f"TOTAL = {self.calculate_total()}")



