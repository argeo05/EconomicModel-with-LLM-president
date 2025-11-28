from dataclasses import dataclass
from typing import Any


@dataclass
class Household:
    income: float
    consumption: float
    propensity_to_consume: float
    labor_sensitivity: float
    n: int = 1
    max_labor_time: float = 1.0
    labor_supply: float = 0.0
    savings: float = 0.0
    desired_consumption: float = 0.0

    def decide_labor(self, wage: float) -> float:
        raw_labor = self.labor_sensitivity * wage
        self.labor_supply = max(0.0, min(self.max_labor_time, raw_labor))
        return self.labor_supply * self.n

    def update_income(self, wage: float, employment: float) -> None:
        self.income = wage * employment

    def decide_consumption(self) -> float:
        self.desired_consumption = self.propensity_to_consume * self.income
        return self.desired_consumption

    def decide_goods_demand(self, price: float) -> float:
        if price <= 0:
            return 0.0
        return self.desired_consumption / price

    def update_consumption(self, actual_goods: float, price: float) -> None:
        actual_spending = actual_goods * price
        self.consumption = actual_spending
        self.savings += self.income - self.consumption
