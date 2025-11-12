from dataclasses import dataclass
from typing import Sequence


@dataclass
class LaborMarket:
    wage: float = 4.35

    def clear_market(
        self,
        labor_supply_list: Sequence[float],
        labor_demand_list: Sequence[float]
    ) -> float:
        total_supply = sum(labor_supply_list)
        total_demand = sum(labor_demand_list)

        if total_supply == 0:
            self.wage = 0.0
            return self.wage

        imbalance = (total_demand - total_supply) / max(total_supply, 1e-6)
        adjustment = 0.03 * imbalance if imbalance > 0 else 0.01 * imbalance
        self.wage = max(0.5, self.wage * (1 + adjustment))
        return self.wage

    def match_labor(
        self,
        labor_supply_list: Sequence[float],
        labor_demand_list: Sequence[float]
    ) -> tuple[list[float], list[float]]:
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
