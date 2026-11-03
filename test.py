from vehicle import EconomyCar, Suv, Luxury
from customer import Customer
from rental import Rental
from payment import Mpesa, PaymentStatus, Card, Cash




# --- build the scenario (one line per object, exactly like your table links them) ---
suv = Suv("KAA-102", "Toyota", "Land Cruiser", 2023, 12000)
alice = Customer("C-001", "Alice", "+254712345678", 34567890, "DL-123")
r = Rental("R-1001", alice, suv, 3)
r.complete_rental(actual_days=5, damage_control=5000)


# --- TEST 1: the happy path ---
print("Bill:", r.calculate_total())            # expect 79000.0
pay = Card("P-9001", r, card_number="9865432712345678")
result = pay.process()

print("process() returned:", result)           # expect True
print("status:", pay.status)                  # expect PaymentStatus.COMPLETED
print("amount:", pay.amount)                   # expect 79000.0  (copied from rental's bill)
print("rental is_paid():", r.is_paid())        # expect True  ← THE critical line





# --- TEST 2: invalid phone → FAILED, rental stays unpaid ---
vitz = EconomyCar("KAA-101", "Toyota", "Vitz", 2022, 3000)
bob = Customer("C-002", "Bob", "0798765432", 45678901, "DL-456")
r2 = Rental("R-1002", bob, vitz, 2)

bad = Card("P-9002", r2, card_number="12345")     # doesn't start with 07
result = bad.process()
print("returned:", result)            # expect False
print("status:", bad.status)          # expect PaymentStatus.FAILED
print("rental paid:", r2.is_paid())   # expect False  ← guard held

