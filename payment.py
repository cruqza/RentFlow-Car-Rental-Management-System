from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from enum import Enum
from typing import Any
from rental import Rental
import string
import random
from abc import ABC, abstractmethod
import re


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
    amount: float = field(init=False)
    transaction_code: str = field(default="", init=False)


    def __post_init__(self):
        self.amount = self.rental.calculate_total()

    @abstractmethod
    def process_payment(self) -> bool:
        pass


    def gen_code(self) -> str:
        return "".join(random.choices(string.ascii_uppercase + string.digits, k=10))

    def fail(self, message : str ) -> bool:
        print(message)
        self.status =  PaymentStatus.FAILED
        return False


    def _settle(self):
        self.status = PaymentStatus.COMPLETED
        # self.transaction_code = self.gen_code()
        self.rental.mark_as_paid()

    def is_completed(self) -> bool:
        return self.status == PaymentStatus.COMPLETED



@dataclass
class MpesaPayment(Payment):
    phone_number: str = ""

    def _gen_code(self) -> str:
        return "".join(random.choices(string.ascii_uppercase + string.digits, k=10))

    def process_payment(self) -> bool:
        if self.is_completed():
            return self._fail("This transaction is already completed")
        if not re.fullmatch(r"(07|01)\d{8}", self.phone_number):
            return self._fail("Invalid Safaricom number.")
        self.transaction_code = self._gen_code()
        self._settle()
        print(f"{self.transaction_code} Confirmed. Ksh {self.amount:,.0f} " 
              f"received from {self.phone_number}.")
        return True


@dataclass
class CardPayment(Payment):
    card_number: str = [":4"]

    def _gen_code(self) -> str:
        digits = "".join(random.choices(string.ascii_uppercase + string.digits, k=10))
        return f"AUTH-{digits}"

    def process_payment(self) -> bool:
        if len(self.card_number) != 16 or not self.card_number.isdigit():
            print("Invalid card number.")
            self.status = PaymentStatus.FAILED
            return False
        print(f"Card ending {self.card_number[-4:]} charged Ksh {self.amount}.")
        self._settle()
        return True


@dataclass
class CashPayment(Payment):
    cash_received: float = 0.0

    def process_payment(self) -> bool:
        if self.cash_received < self.amount:
            print(f"Insufficient: need {self.amount}, received {self.cash_received}.")
            self.status = PaymentStatus.FAILED
            return False
        change = self.cash_received - self.amount
        if change > 0:
            print(f"Give change: {change}.")
        self._settle()
        return True


