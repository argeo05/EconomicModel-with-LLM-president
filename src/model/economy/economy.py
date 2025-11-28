from dataclasses import dataclass, field
from typing import List
from ..agents import Household, Firm
from ..institutions import CentralBank, LaborMarket, GoodsMarket
from .state import EconomyState


@dataclass
class Economy:
    households: List[Household]
    firms: List[Firm]
    central_bank: CentralBank
    labor_market: LaborMarket
    goods_market: GoodsMarket
    state: EconomyState
    tech_progress_rate: float = 0.005

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

        for h, labor in zip(self.households, actual_employed):
            h.update_income(new_wage, labor)
            h.decide_consumption()

        goods_supply = [f.decide_goods_supply() for f in self.firms]
        goods_demand = [h.decide_goods_demand(self.goods_market.price) for h in self.households]

        new_price = self.goods_market.clear_market(goods_supply, goods_demand)
        actual_sold, actual_buy = self.goods_market.match_goods(goods_supply, goods_demand)

        for h, bought in zip(self.households, actual_buy):
            h.update_consumption(bought, new_price)

        for firm, sold, labor in zip(self.firms, actual_sold, actual_demand):
            firm.update_sales(sold, new_price, new_wage, labor)

        if self.state.price_level > 0:
            inflation = (new_price - self.state.price_level) / self.state.price_level
        else:
            inflation = 0.0
        
        price_level = new_price

        for firm in self.firms:
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
