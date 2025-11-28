from dataclasses import dataclass
from typing import Sequence


@dataclass
class LaborMarket:
    """Labor market clearing mechanism.

    Attributes:
        wage: Current wage rate
    """
    wage: float

    def clear_market(
        self,
        labor_supply_list: Sequence[float],
        labor_demand_list: Sequence[float]
    ) -> float:
        """Adjust wage based on supply and demand.

        Args:
            labor_supply_list: Labor supply from households
            labor_demand_list: Labor demand from firms

        Returns:
            New wage rate
        """
        total_supply = sum(labor_supply_list)
        total_demand = sum(labor_demand_list)

        if total_supply == 0:
            self.wage = 0.0
            return self.wage

        imbalance = (total_demand - total_supply) / max(total_supply, 1e-6)
        adjustment = 0.10 * imbalance
        self.wage = max(1.0, self.wage * (1 + adjustment))
        return self.wage

    def match_labor(
        self, 
        labor_supply_list: Sequence[float], 
        labor_demand_list: Sequence[float]
    ) -> tuple[list[float], list[float]]:
        """Match labor supply and demand.

        Args:
            labor_supply_list: Labor supply from households
            labor_demand_list: Labor demand from firms

        Returns:
            Tuple of actual employment and actual demand lists
        """
        total_supply = sum(labor_supply_list)
        total_demand = sum(labor_demand_list)

        if total_demand <= 0 or total_supply <= 0:
            return [0.0] * len(labor_supply_list), [0.0] * len(labor_demand_list)

        if total_demand >= total_supply:
            actual_employed = [ls for ls in labor_supply_list]
            ratio = total_supply / total_demand
            actual_demand = [ld * ratio for ld in labor_demand_list]
        else:
            ratio = total_demand / total_supply
            actual_employed = [ls * ratio for ls in labor_supply_list]
            actual_demand = [ld for ld in labor_demand_list]
        
        return actual_employed, actual_demand
