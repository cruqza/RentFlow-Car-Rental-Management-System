from vehicle import Vehicle
from customer import Customer
from rental import Rental, RentalStatus
from payment import Payment


class CarRentalSystem:
    def __init__(self):
        self.name = "SafariDrive Rentals"
        self.vehicles = []
        self.customers = []
        self.rentals = []
        self.payments = []
        self.__revenue = 0            
        self._next_rental_number = 1

    #-----------Adding Fleet and customers -----------------------------------------
    def add_vehicle(self, vehicle: Vehicle) -> None:
        if self.find_vehicle(vehicle.registration_number):
            raise ValueError(f"Vehicle {vehicle.registration_number} already exists.")
        self.vehicles.append(vehicle)

    def register_customer(self, customer: Customer) -> None:
        if self.find_customer(customer.customer_id):
            raise ValueError(f"Customer {customer.customer_id} already registered.")
        self.customers.append(customer)

    def find_vehicle(self, registration_number: str):
        for vehicle in self.vehicles:
            if vehicle.registration_number == registration_number:
                return vehicle
        return "Vehicle not found"

    def find_customer(self, customer_id):
        for customer in self.customers:
            if customer.customer_id == customer_id:
                return customer
        return "Customer not found."

    # ---------- Searching ----------
    def show_available_vehicles(self) -> None:
        available = [v for v in self.vehicles if v.is_available()]
        if not available:
            print("No vehicles available.")
            return
        for v in available:
            print(f"{v.registration_number} | {v.make} {v.model} ({v.year}) "
                  f"| KSh {v.daily_rate:,.0f}/day")

    def search_vehicles(self, vehicle_type=None, max_daily_rate=None) -> list:
        results = [v for v in self.vehicles if v.is_available()]
        if vehicle_type is not None:
            if isinstance(vehicle_type, str):
                results = [v for v in results
                           if type(v).__name__.lower() == vehicle_type.lower()]
            else:                                   # a class, e.g. Suv
                results = [v for v in results if isinstance(v, vehicle_type)]
        if max_daily_rate is not None:
            results = [v for v in results if v.daily_rate <= max_daily_rate]
        return results

    # ---------- Rentals ----------
    def rent_vehicle(self, customer: Customer, vehicle: Vehicle, days: int) -> Rental:
        if customer not in self.customers:
            raise ValueError("Customer is not registered.")
        if vehicle not in self.vehicles:
            raise ValueError("Vehicle is not in the fleet.")
        if days <= 0:
            raise ValueError("Rental days must be at least 1.")
        if not vehicle.is_available():
            raise ValueError(f"Vehicle {vehicle.registration_number} is not available.")

        rental = Rental(f"R{self._next_rental_number:04d}", customer, vehicle, days)
        self._next_rental_number += 1
        vehicle.mark_as_rented()
        self.rentals.append(rental)
        return rental

    def return_vehicle(self, rental: Rental, actual_days: int, damage_charge: float = 0) -> None:
        if rental not in self.rentals:
            raise ValueError("Rental does not belong to this system.")
        if rental.status != RentalStatus.ACTIVE:
            raise ValueError("Rental is not active.")
        if actual_days <= 0:
            raise ValueError("Actual days must be at least 1.")
        if damage_charge < 0:
            raise ValueError("Damage charge cannot be negative.")

        rental.complete(actual_days, damage_charge)
        rental.vehicle.mark_as_available()

    # ---------- Payments ----------
    def process_payment(self, payment: Payment) -> bool:
        if payment.rental not in self.rentals:
            raise ValueError("Payment is for a rental outside this system.")
        self.payments.append(payment)
        success = payment.process_payment()
        if success:
            self.__revenue += payment.amount
        return success

    # ---------- Reports ----------
    def show_active_rentals(self) -> None:
        self._show_rentals(RentalStatus.ACTIVE, "active")

    def show_completed_rentals(self) -> None:
        self._show_rentals(RentalStatus.COMPLETED, "completed")

    def _show_rentals(self, status, label: str) -> None:
        rentals = [r for r in self.rentals if r.status == status]
        if not rentals:
            print(f"No {label} rentals.")
            return
        for r in rentals:
            print(r)

    @property
    def revenue(self) -> float:
        return self.__revenue

    def generate_report(self) -> None:
        available = sum(1 for v in self.vehicles if v.is_available())
        active = sum(1 for r in self.rentals if r.status == RentalStatus.ACTIVE)
        completed = sum(1 for r in self.rentals if r.status == RentalStatus.COMPLETED)
        paid = sum(1 for p in self.payments if p.is_completed())
        failed = len(self.payments) - paid

        print(f"===== {self.name} - Management Report =====")
        print(f"Fleet size        : {len(self.vehicles)}")
        print(f"  Available       : {available}")
        print(f"  Rented out      : {len(self.vehicles) - available}")
        print(f"Customers         : {len(self.customers)}")
        print(f"Rentals           : {len(self.rentals)} "
              f"({active} active, {completed} completed)")
        print(f"Payments          : {paid} successful, {failed} failed")
        print(f"Total revenue     : KSh {self.revenue:,.0f}")