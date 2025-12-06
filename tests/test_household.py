import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.model.agents.household import Household


def test_household_initialization():
    household = Household(
        income=100.0,
        consumption=80.0,
        propensity_to_consume=0.8,
        labor_sensitivity=0.5,
        n=10
    )
    assert household.income == 100.0
    assert household.consumption == 80.0
    assert household.n == 10
    assert household.savings == 0.0


def test_decide_labor():
    household = Household(
        income=0.0,
        consumption=0.0,
        propensity_to_consume=0.8,
        labor_sensitivity=0.5,
        n=10,
        max_labor_time=1.0
    )
    total_labor = household.decide_labor(wage=1.5)
    assert household.labor_supply == 0.75
    assert total_labor == 7.5
    
    total_labor_max = household.decide_labor(wage=5.0)
    assert household.labor_supply == 1.0
    assert total_labor_max == 10.0


def test_update_income_and_consumption():
    household = Household(income=0.0, consumption=0.0, propensity_to_consume=0.8, labor_sensitivity=0.5, savings=0.0)
    household.update_income(wage=10.0, employment=8.0)
    assert household.income == 80.0
    
    household.update_consumption(actual_goods=20.0, price=2.0)
    assert household.consumption == 40.0
    assert household.savings == 40.0


def test_decide_consumption_and_goods_demand():
    household = Household(
        income=100.0,
        consumption=0.0,
        propensity_to_consume=0.8,
        labor_sensitivity=0.5,
        savings=50.0,
        interest_rate_sensitivity=0.5,
        savings_usage=0.1
    )
    desired = household.decide_consumption(interest_rate=0.05)
    assert desired > 0
    assert household.desired_consumption == desired
    
    demand = household.decide_goods_demand(price=2.0)
    assert demand == desired / 2.0
    
    demand_zero = household.decide_goods_demand(price=0.0)
    assert demand_zero == 0.0
