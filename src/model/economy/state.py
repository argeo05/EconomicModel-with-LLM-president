from dataclasses import dataclass
from typing import Optional


@dataclass
class EconomyState:
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
        self.period += 1
        self.output = new_output
        self.inflation = new_inflation
        self.unemployment = new_unemployment
        self.interest_rate = new_interest_rate
        self.wage = new_wage
        self.price_level = new_price_level

    @staticmethod
    def initial(config: Optional[dict] = None) -> "EconomyState":
        return EconomyState(
            period=config.get("period", 0),
            output=config.get("output", 680.0),
            inflation=config.get("inflation", 0.02),
            unemployment=config.get("unemployment", 0.05),
            interest_rate=config.get("interest_rate", 0.025),
            wage=config.get("wage"),
            price_level=config.get("price_level")
        )