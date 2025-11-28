from dataclasses import dataclass
from typing import Optional


@dataclass
class EconomyState:
    """Economic state variables.

    Attributes:
        period: Current period number
        output: Aggregate output
        inflation: Inflation rate
        unemployment: Unemployment rate
        interest_rate: Interest rate
        wage: Wage rate
        price_level: Price level
    """
    period: int
    output: float
    inflation: float
    unemployment: float
    interest_rate: float
    wage: float
    price_level: float

    def update(
        self,
        new_output: float,
        new_inflation: float,
        new_unemployment: float,
        new_interest_rate: float,
        new_wage: float,
        new_price_level: float
    ) -> None:
        """Update state variables.

        Args:
            new_output: New output value
            new_inflation: New inflation rate
            new_unemployment: New unemployment rate
            new_interest_rate: New interest rate
            new_wage: New wage rate
            new_price_level: New price level
        """
        self.period += 1
        self.output = new_output
        self.inflation = new_inflation
        self.unemployment = new_unemployment
        self.interest_rate = new_interest_rate
        self.wage = new_wage
        self.price_level = new_price_level

    @staticmethod
    def initial(config: Optional[dict] = None) -> "EconomyState":
        """Create initial state from config.

        Args:
            config: Configuration dictionary

        Returns:
            Initial economy state
        """
        return EconomyState(
            period=config.get("period", 0),
            output=config.get("output", 680.0),
            inflation=config.get("inflation", 0.02),
            unemployment=config.get("unemployment", 0.05),
            interest_rate=config.get("interest_rate", 0.025),
            wage=config.get("wage"),
            price_level=config.get("price_level")
        )