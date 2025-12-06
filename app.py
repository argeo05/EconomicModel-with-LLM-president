import argparse
from src import (
    Household,
    Firm,
    CentralBank,
    LaborMarket,
    GoodsMarket,
    Economy,
    EconomyState,
    Plots,
    load_config
)
from src.visualization import DataEconomyHandler
from src.model.agents import Households


def run_simulation(years: int, config_path: str, llm_based_president: bool, llm_based_households: bool) -> DataEconomyHandler:
    config = load_config(config_path)

    households: Households = Households()
    for class_config in config["households"]:
        households.append(
            Household(
                income=0.0,
                consumption=0.0,
                propensity_to_consume=class_config["propensity_to_consume"],
                labor_sensitivity=class_config["labor_sensitivity"],
                max_labor_time=class_config["max_labor_time"],
                n=class_config["n"],
                savings=class_config.get("initial_savings", 0.0)
            )
        )

    firms = []
    for firm_config in config["firms"]:
        firms.append(
            Firm(
                capital=firm_config["capital"],
                alpha=firm_config["alpha"],
                productivity=firm_config["productivity"],
                n=firm_config["n"]
            )
        )

    cb = CentralBank(
        r=config["central_bank"]["r"],
        r_star=config["central_bank"]["r_star"],
        pi_star=config["central_bank"]["pi_star"],
        Y_star=config["central_bank"]["Y_star"],
        phi_pi=config["central_bank"]["phi_pi"],
        phi_y=config["central_bank"]["phi_y"]
    )

    initial_state = config.get("initial_state", {})
    labor_market = LaborMarket(initial_state["wage"])
    goods_market = GoodsMarket(price=config["goods_market"]["initial_price"])
    data_base = DataEconomyHandler().initialize_data_base()
    plots = Plots()

    economy = Economy(
        households=households,
        firms=firms,
        central_bank=cb,
        labor_market=labor_market,
        goods_market=goods_market,
        state=EconomyState.initial(initial_state),
        llm_based_president=llm_based_president,
        llm_based_households=llm_based_households,
    )

    for _ in range(years):
        economy.step()
        s = economy.state
        data_base.append(s.output, s.inflation, s.unemployment, s.interest_rate, s.wage)
        plots.update(s.period, s.output, s.inflation, s.unemployment, s.interest_rate, s.wage)
        print(
            f"Период {s.period:3d} | "
            f"Y={s.output:8.2f} | π={s.inflation:6.2%} | u={s.unemployment:6.2%} | "
            f"r={s.interest_rate:6.2%} | w={s.wage:6.2f}"
        )
    plots.show()
    return data_base


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("years", type=int, help="number of years", default=10)
    parser.add_argument("--llm-based-president", action="store_true", help="use LLM for president decisions")
    parser.add_argument("--llm-based-households", action="store_true", help="use LLM for household decisions")
    parser.add_argument("--config", type=str, help="path to config file", default="config.yaml")
    args = parser.parse_args()

    run_simulation(years=args.years, config_path=args.config,
                                    llm_based_president=args.llm_based_president,
                                    llm_based_households=args.llm_based_households)


if __name__ == "__main__":
    main()
