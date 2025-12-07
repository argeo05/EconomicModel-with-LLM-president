import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.model.institutions.labor_market import LaborMarket


def test_labor_market_clear_market():
    market = LaborMarket(wage=10.0)
    
    new_wage = market.clear_market(
        labor_supply_list=[100.0, 150.0],
        labor_demand_list=[200.0, 100.0]
    )
    assert market.wage >= 1.0
    assert new_wage > 10.0
    
    market.wage = 10.0
    low_wage = market.clear_market(
        labor_supply_list=[200.0, 150.0],
        labor_demand_list=[100.0, 50.0]
    )
    assert low_wage < 10.0
    
    market.clear_market(labor_supply_list=[0.0], labor_demand_list=[100.0])
    assert market.wage == 0.0


def test_labor_market_match_labor():
    market = LaborMarket(wage=10.0)
    
    employed, demand = market.match_labor(
        labor_supply_list=[100.0, 100.0],
        labor_demand_list=[150.0, 150.0]
    )
    assert sum(employed) == 200.0
    assert sum(demand) == 200.0
    
    employed, demand = market.match_labor(
        labor_supply_list=[200.0, 200.0],
        labor_demand_list=[150.0, 150.0]
    )
    assert sum(employed) == 300.0
    assert sum(demand) == 300.0
    
    employed, demand = market.match_labor(
        labor_supply_list=[0.0],
        labor_demand_list=[100.0]
    )
    assert sum(employed) == 0.0
    assert sum(demand) == 0.0
