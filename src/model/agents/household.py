from dataclasses import dataclass
from typing import Any


@dataclass
class Household:
    """Consumer agent.

    Attributes:
        income: Income earned
        consumption: Consumption spending
        propensity_to_consume: Marginal propensity to consume
        labor_sensitivity: Labor supply wage sensitivity
        n: Number of identical households
        max_labor_time: Maximum labor time available
        labor_supply: Labor supply quantity
        savings: Accumulated savings
        desired_consumption: Desired consumption amount
    """
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
        """Decide labor supply based on wage.

        Args:
            wage: Wage rate

        Returns:
            Total labor supply across all households
        """
        raw_labor = self.labor_sensitivity * wage
        self.labor_supply = max(0.0, min(self.max_labor_time, raw_labor))
        return self.labor_supply * self.n

    def update_income(self, wage: float, employment: float) -> None:
        """Update income from employment.

        Args:
            wage: Wage rate
            employment: Employment quantity
        """
        self.income = wage * employment

    def decide_consumption(self) -> float:
        """Decide desired consumption.

        Returns:
            Desired consumption amount
        """
        available_funds = self.income + max(0.0, self.savings * 0.05)
        self.desired_consumption = self.propensity_to_consume * available_funds
        return self.desired_consumption

    def decide_goods_demand(self, price: float) -> float:
        """Calculate goods demand quantity.

        Args:
            price: Goods price

        Returns:
            Quantity of goods demanded
        """
        if price <= 0:
            return 0.0
        return self.desired_consumption / price

    def update_consumption(self, actual_goods: float, price: float) -> None:
        """Update consumption and savings.

        Args:
            actual_goods: Actual goods purchased
            price: Goods price
        """
        actual_spending = actual_goods * price
        self.consumption = actual_spending
        self.savings += self.income - self.consumption
