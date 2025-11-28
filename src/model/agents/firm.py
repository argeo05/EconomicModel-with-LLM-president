from dataclasses import dataclass
from typing import Any


@dataclass
class Firm:
    """Production unit agent.

    Attributes:
        capital: Capital stock
        alpha: Capital elasticity in Cobb-Douglas production
        productivity: Total factor productivity
        n: Number of identical firms
        labor_demand: Labor demand quantity
        output: Production output
        profit: Profit value
        investment_rate: Share of profit invested
        depreciation_rate: Capital depreciation rate
    """
    capital: float
    alpha: float
    productivity: float
    n: int = 1
    labor_demand: float = 0.0
    output: float = 0.0
    profit: float = 0.0
    investment_rate: float = 0.25
    depreciation_rate: float = 0.025

    def decide_labor_demand(self, wage: float) -> float:
        """Calculate optimal labor demand.

        Args:
            wage: Wage rate

        Returns:
            Total labor demand across all firms
        """
        if wage <= 0:
            self.labor_demand = 0.0
        else:
            mpl_coef = (1 - self.alpha) * self.productivity
            base = mpl_coef * (self.capital ** self.alpha) / wage
            self.labor_demand = base ** (1 / (1 + self.alpha))
        return max(0.01, self.labor_demand * self.n)

    def produce(self, labor: float) -> float:
        """Produce output using Cobb-Douglas function.

        Args:
            labor: Labor input

        Returns:
            Total output produced
        """
        labor_per_firm = labor / self.n if self.n > 0 else 0.0
        self.output = self.productivity * (self.capital ** self.alpha) * (labor_per_firm ** (1 - self.alpha))
        return self.output * self.n

    def update_profit(self, price: float, wage: float, labor: float) -> None:
        """Update profit based on revenue and costs.

        Args:
            price: Goods price
            wage: Wage rate
            labor: Labor employed
        """
        labor_per_firm = labor / self.n if self.n > 0 else 0.0
        revenue = price * self.output
        cost = wage * labor_per_firm
        self.profit = revenue - cost

    def update_capital(self, interest_rate: float) -> None:
        """Update capital stock with investment and depreciation.

        Args:
            interest_rate: Interest rate affecting investment
        """
        rate_factor = max(0.6, 1.1 - 4.0 * (interest_rate - 0.03))
        investment = max(0.0, self.profit * self.investment_rate * rate_factor)
        depreciation = self.capital * self.depreciation_rate
        self.capital = max(1.0, self.capital + investment - depreciation)

    def decide_goods_supply(self) -> float:
        """Decide goods supply quantity.

        Returns:
            Output quantity to supply
        """
        return self.output

    def update_sales(self, actual_sold: float, price: float, wage: float, labor: float) -> None:
        """Update profit based on actual sales.

        Args:
            actual_sold: Actual quantity sold
            price: Goods price
            wage: Wage rate
            labor: Labor employed
        """
        actual_sold_per_firm = actual_sold / self.n if self.n > 0 else 0.0
        labor_per_firm = labor / self.n if self.n > 0 else 0.0
        revenue = price * actual_sold_per_firm
        cost = wage * labor_per_firm
        self.profit = revenue - cost