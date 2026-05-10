import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.model.economy.state import EconomyState


def test_economy_state_initialization():
    state = EconomyState(
        period=0,
        output=700.0,
        inflation=0.02,
        unemployment=0.05,
        interest_rate=0.03,
        wage=12.0,
        price_level=1.0
    )
    assert state.period == 0
    assert state.output == 700.0
    assert state.inflation == 0.02


def test_economy_state_update():
    state = EconomyState(
        period=0,
        output=700.0,
        inflation=0.02,
        unemployment=0.05,
        interest_rate=0.03,
        wage=12.0,
        price_level=1.0
    )
    
    state.update(
        new_output=720.0,
        new_inflation=0.025,
        new_unemployment=0.04,
        new_interest_rate=0.035,
        new_wage=12.5,
        new_price_level=1.02,
        president_message="Bla-bla-bla"
    )
    
    assert state.period == 1
    assert state.output == 720.0
    assert state.inflation == 0.025
    assert state.president_message == "Bla-bla-bla"

