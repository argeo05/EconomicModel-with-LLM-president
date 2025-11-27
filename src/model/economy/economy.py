from dataclasses import dataclass, field
from typing import List
from ..agents.household import Household
from ..agents.firm import Firm
from ..institutions.central_bank import CentralBank
from ..institutions.labor_market import LaborMarket
from .state import EconomyState


@dataclass
class Economy:
    households: List[Household]
    firms: List[Firm]
    central_bank: CentralBank
    labor_market: LaborMarket
    state: EconomyState
    tech_progress_rate: float = 0.001

    def step(self) -> None:
        labor_supply = [h.decide_labor(self.state.wage) for h in self.households]
        labor_demand = [f.decide_labor_demand(self.state.wage) for f in self.firms]

        new_wage = self.labor_market.clear_market(labor_supply, labor_demand)
        actual_employed, actual_demand = self.labor_market.match_labor(labor_supply, labor_demand)

        total_labor_supply = sum(labor_supply)
        total_employment = sum(actual_employed)
        unemployment = max(0.0, (total_labor_supply - total_employment) / max(total_labor_supply, 1e-6))

        total_output = 0.0
        for firm, labor in zip(self.firms, actual_demand):
            total_output += firm.produce(labor)

        if self.state.output > 0:
            output_gap = (total_output - self.state.output) / self.state.output
            inflation = 0.75 * self.state.inflation + 0.1 * output_gap + 0.003
        else:
            inflation = 0.0
        
        price_level = self.state.price_level * (1 + inflation)

        for h, labor in zip(self.households, actual_employed):
            h.update_income(new_wage, labor)
            h.decide_consumption()

        for firm, labor in zip(self.firms, actual_demand):
            firm.update_profit(price_level, new_wage, labor)
            firm.update_capital(self.state.interest_rate)
            firm.productivity *= (1 + self.tech_progress_rate)

        new_rate = self.central_bank.propose_rate(inflation, total_output)

        self.state.update(
            new_output=total_output,
            new_inflation=inflation,
            new_unemployment=unemployment,
            new_interest_rate=new_rate,
            new_wage=new_wage,
            new_price_level=price_level
        )
