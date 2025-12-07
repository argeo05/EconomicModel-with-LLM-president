import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.model.institutions.goods_market import GoodsMarket


def test_goods_market_clear_market():
    market = GoodsMarket(price=1.0)
    
    new_price = market.clear_market(
        goods_supply_list=[100.0, 150.0],
        goods_demand_list=[200.0, 100.0]
    )
    assert market.price >= 0.5
    assert new_price > 1.0
    
    market.price = 1.0
    low_price = market.clear_market(
        goods_supply_list=[200.0, 150.0],
        goods_demand_list=[100.0, 50.0]
    )
    assert low_price < 1.0
    
    market.clear_market(goods_supply_list=[0.0], goods_demand_list=[100.0])
    assert market.price == 1.0


def test_goods_market_match_goods():
    market = GoodsMarket(price=1.0)
    
    sold, buy = market.match_goods(
        goods_supply_list=[100.0, 100.0],
        goods_demand_list=[150.0, 150.0]
    )
    assert sum(sold) == 200.0
    assert sum(buy) == 200.0
    
    sold, buy = market.match_goods(
        goods_supply_list=[200.0, 200.0],
        goods_demand_list=[150.0, 150.0]
    )
    assert sum(sold) == 300.0
    assert sum(buy) == 300.0
    
    sold, buy = market.match_goods(
        goods_supply_list=[0.0],
        goods_demand_list=[100.0]
    )
    assert sum(sold) == 0.0
    assert sum(buy) == 0.0
