import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.model.agents.firm import Firm


def test_firm_initialization():
    firm = Firm(
        capital=100.0,
        alpha=0.3,
        productivity=1.5,
        n=5
    )
    assert firm.capital == 100.0
    assert firm.alpha == 0.3
    assert firm.n == 5
    assert firm.output == 0.0
    assert firm.profit == 0.0


def test_decide_labor_demand():
    firm = Firm(
        capital=100.0,
        alpha=0.3,
        productivity=1.5,
        n=5
    )
    total_labor = firm.decide_labor_demand(wage=10.0, interest_rate=0.05)
    assert firm.labor_demand > 0
    assert total_labor > 0
    
    firm.decide_labor_demand(wage=0.0)
    assert firm.labor_demand == 0.0


def test_produce():
    firm = Firm(
        capital=100.0,
        alpha=0.3,
        productivity=1.5,
        n=5
    )
    total_output = firm.produce(labor=50.0)
    assert firm.output > 0
    assert total_output == firm.output * 5


def test_update_profit_and_capital():
    firm = Firm(
        capital=100.0,
        alpha=0.3,
        productivity=1.5,
        n=5,
        investment_rate=0.25,
        depreciation_rate=0.025
    )
    firm.produce(labor=50.0)
    firm.update_profit(price=2.0, wage=10.0, labor=50.0)
    assert firm.profit != 0.0
    
    initial_capital = firm.capital
    firm.update_capital(interest_rate=0.05)
    assert firm.capital != initial_capital
    assert firm.capital >= 1.0


def test_goods_supply_and_sales():
    firm = Firm(
        capital=100.0,
        alpha=0.3,
        productivity=1.5,
        n=5
    )
    firm.produce(labor=50.0)
    supply = firm.decide_goods_supply()
    assert supply == firm.output
    
    firm.update_sales(actual_sold=supply * 5, price=2.0, wage=10.0, labor=50.0)
    assert firm.profit != 0.0
