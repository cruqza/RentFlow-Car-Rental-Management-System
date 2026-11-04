from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from enum import Enum
from typing import Any
import re
from abc import ABC, abstractmethod





@dataclass
class Vehicle(ABC):
        
    registration_number : str
    make : str
    model : str
    year : int
    daily_rate : float
    _available : bool = field(default=True, init=False)

    def __post_init__(self):
        if self.daily_rate < 0:
            raise ValueError("Daily rate cannot be negative.")

    def is_available(self):
        return self._available

    def mark_as_rented(self):
        self._available = False

    def mark_as_available(self):
        self._available = True

    @abstractmethod
    def rental_cost(self, days: int) -> float:
        pass 

class EconomyCar(Vehicle):
    def rental_cost(self, days) -> float:
        return self.daily_rate * days   


class Suv(Vehicle):
    SERVICE_CHARGE = 2000
    def rental_cost(self, days: int) -> float:
        return self.daily_rate * days + self.SERVICE_CHARGE

class Luxury(Vehicle):
    def rental_cost(self, days: int) -> float:
        subtotal = self.daily_rate * days
        return subtotal * 1.1


