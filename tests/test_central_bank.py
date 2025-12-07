import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.model.institutions.central_bank import CentralBank


def test_central_bank_propose_rate():
    bank = CentralBank(
        r=0.02,
        r_star=0.03,
        pi_star=0.02,
        Y_star=100.0,
        phi_pi=1.5,
        phi_y=0.5,
        r_min=0.0,
        r_max=0.10,
        adjustment_speed=0.3
    )
    
    new_rate = bank.propose_rate(inflation=0.03, output=105.0)
    assert bank.r >= bank.r_min
    assert bank.r <= bank.r_max
    assert new_rate == bank.r
    
    low_rate = bank.propose_rate(inflation=0.01, output=95.0)
    assert low_rate < new_rate
