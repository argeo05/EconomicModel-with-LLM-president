from typing import List
from ..agents import Household, Firm, President, Households
from ..institutions import CentralBank, LaborMarket, GoodsMarket
from .state import EconomyState


class Economy:
    """Economic system simulation.

    Attributes:
        households: List of household agents
        firms: List of firm agents
        central_bank: Central bank institution
        labor_market: Labor market institution
        goods_market: Goods market institution
        state: Current economy state
        tech_progress_rate: Technological progress rate
        llm_based_president: If true use llm for president, else only rules
        llm_based_households: If true use llm for households, else only rules
    """

    def __init__(self, households: Households, firms: List[Firm], central_bank: CentralBank,
                 labor_market: LaborMarket, goods_market: GoodsMarket, state: EconomyState,
                 llm_based_president: bool, llm_based_households: bool, tech_progress_rate: float = 0.005):
        self.households = households
        self.firms = firms
        self.central_bank = central_bank
        self.labor_market = labor_market
        self.goods_market = goods_market
        self.state = state
        self.tech_progress_rate = tech_progress_rate
        self.llm_based_president = llm_based_president
        self.llm_based_households = llm_based_households

    def step(self) -> None:
        """Execute one simulation period."""

        labor_supply = self.households.decide_labors(self.state.wage, self.llm_based_households)
        labor_demand = [f.decide_labor_demand(self.state.wage, self.state.interest_rate) for f in self.firms]

        actual_employed, actual_demand = self.labor_market.match_labor(labor_supply, labor_demand)

        total_labor_supply = sum(labor_supply)
        total_employment = sum(actual_employed)
        unemployment = max(0.0, (total_labor_supply - total_employment) / max(total_labor_supply, 1e-6))

        total_output = 0.0
        for firm, labor in zip(self.firms, actual_demand):
            total_output += firm.produce(labor)

        for h, labor in zip(self.households.households, actual_employed):
            h.update_income(self.state.wage, labor)
        self.households.decide_consumptions(self.state.interest_rate, self.llm_based_households)

        goods_supply = [f.decide_goods_supply() for f in self.firms]
        goods_demand = [h.decide_goods_demand(self.goods_market.price) for h in self.households.households]

        actual_sold, actual_buy = self.goods_market.match_goods(goods_supply, goods_demand)

        for h, bought in zip(self.households.households, actual_buy):
            h.update_consumption(bought, self.state.price_level)

        for firm, sold, labor in zip(self.firms, actual_sold, actual_demand):
            firm.update_sales(sold, self.state.price_level, self.state.wage, labor)

        new_price = self.goods_market.clear_market(goods_supply, goods_demand)
        if self.state.price_level > 0:
            inflation = (new_price - self.state.price_level) / self.state.price_level
        else:
            inflation = 0.0

        for firm in self.firms:
            firm.update_capital(self.state.interest_rate)
            firm.productivity *= (1 + self.tech_progress_rate)

        new_rate = self.central_bank.propose_rate(inflation, total_output)
        if self.llm_based_president:
            president_answer = President.make_decision(
                y_star=self.central_bank.Y_star,
                inflation=inflation,
                output=total_output,
                unemployment=unemployment,
                supply_goods=sum(goods_supply),
                demand_goods=sum(goods_demand),
                r_central_bank=new_rate
            )
            new_rate = president_answer.new_interest_rate
            self.households.president_advice = president_answer.advice

        new_wage = self.labor_market.clear_market(labor_supply, labor_demand)
        self.state.update(
            new_output=total_output,
            new_inflation=inflation,
            new_unemployment=unemployment,
            new_interest_rate=new_rate,
            new_wage=new_wage,
            new_price_level=new_price
        )