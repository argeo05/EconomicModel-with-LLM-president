from dataclasses import dataclass
from typing import Sequence


@dataclass
class GoodsMarket:
    """Goods market clearing mechanism.

    Attributes:
        price: Current price level
    """
    price: float

    def clear_market(
        self,
        goods_supply_list: Sequence[float],
        goods_demand_list: Sequence[float]
    ) -> float:
        """Adjust price based on supply and demand.

        Args:
            goods_supply_list: Goods supply from firms
            goods_demand_list: Goods demand from households

        Returns:
            New price level
        """
        total_supply = sum(goods_supply_list)
        total_demand = sum(goods_demand_list)

        if total_supply == 0:
            self.price = 1.0
            return self.price

        imbalance = (total_demand - total_supply) / max(total_supply, 1e-6)
        adjustment = 0.05 * imbalance
        self.price = max(0.5, self.price * (1 + adjustment))
        return self.price

    def match_goods(
            self, 
            goods_supply_list: Sequence[float],
            goods_demand_list: Sequence[float]
        ) -> tuple[list[float], list[float]]:
        """Match goods supply and demand.

        Args:
            goods_supply_list: Goods supply from firms
            goods_demand_list: Goods demand from households

        Returns:
            Tuple of actual sold and actual buy lists
        """
        total_supply = sum(goods_supply_list)
        total_demand = sum(goods_demand_list)

        if total_demand <= 0 or total_supply <= 0:
            return [0.0] * len(goods_supply_list), [0.0] * len(goods_demand_list)

        if total_demand >= total_supply:
            actual_sold = [gs for gs in goods_supply_list]
            ratio = total_supply / total_demand
            actual_buy = [gd * ratio for gd in goods_demand_list]
        else:
            ratio = total_demand / total_supply
            actual_sold = [gs * ratio for gs in goods_supply_list]
            actual_buy = [gd for gd in goods_demand_list]
        
        return actual_sold, actual_buy