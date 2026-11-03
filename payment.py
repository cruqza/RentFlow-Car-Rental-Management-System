from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from enum import Enum
from typing import Any
from rental import Rental
import string
import random
from abc import ABC, abstractmethod


class PaymentStatus(Enum):
    COMPLETED = "completed"
    FAILED = "failed"
    PENDING  = "pending"

@dataclass
class Payment(ABC):
    payment_id : str
    rental : Rental
    payment_date: date = field(default_factory=date.today)
    status : PaymentStatus = PaymentStatus.PENDING
    amount: float = 0.0
    transaction_code: str = ""


    def __post_init__(self):
        self.amount = self.rental.calculate_total()

    @abstractmethod
    def process(self) -> bool:
        pass


    def gen_code(self) -> str:
        return
    "".join(random.choices(string.ascii_uppercase + string.digits, k=10))




    def _settle(self):
        self.status = PaymentStatus.COMPLETED
        self.transaction_code = self.gen_code()
        self.rental.mark_as_paid()

    def is_completed(self) -> bool:
        return self.status == PaymentStatus.COMPLETED



@dataclass
class Mpesa(Payment):
    phone_number: str = ""

    def _gen_code(self) -> str:
        return
    "".join(random.choices(string.ascii_uppercase + string.digits, k=10))

    def process(self) -> bool:
        if not self.phone_number.startswith("07"):
            print("Invalid Safaricom number.")
            self.status = PaymentStatus.FAILED
            return False
        print(f"STK push to {self.phone_number} — awaiting PIN confirmation...")
        self._settle()
        return True


@dataclass
class Card(Payment):
    card_number: str = ""

    def _gen_code(self) -> str:
        digits = "".join(random.choices(string.digits, k=6))
        return f"AUTH-{digits}"

    def process(self) -> bool:
        if len(self.card_number) != 16 or not self.card_number.isdigit():
            print("Invalid card number.")
            self.status = PaymentStatus.FAILED
            return False
        print(f"Card ...{self.card_number[-4:]} charged {self.amount}.")
        self._settle()
        return True


@dataclass
class Cash(Payment):
    cash_received: float = 0.0

    def process(self) -> bool:
        if self.cash_received < self.amount:
            print(f"Insufficient: need {self.amount}, received {self.cash_received}.")
            self.status = PaymentStatus.FAILED
            return False
        change = self.cash_received - self.amount
        if change > 0:
            print(f"Give change: {change}.")
        self._settle()
        return True
