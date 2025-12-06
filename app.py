import argparse
from src import (
    Household,
    Firm,
    CentralBank,
    LaborMarket,
    GoodsMarket,
    Economy,
    EconomyState,
    load_config,
    plot_all_analytics
)
from src.model.agents import Households


def run_simulation(years: int, config_path: str, llm_based_president: bool, llm_based_households: bool) -> list[dict[str, float]]:
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
    economy = Economy(
        households=households,
        firms=firms,
        central_bank=cb,
        labor_market=labor_market,
        goods_market=goods_market,
        state=EconomyState.initial(initial_state),
        llm_based_president=llm_based_president,
        llm_based_households=llm_based_households
    )

    history = []
    for _ in range(years):
        economy.step()
        s = economy.state
        history.append({
            "period": s.period,
            "output": s.output,
            "inflation": s.inflation,
            "unemployment": s.unemployment,
            "rate": s.interest_rate,
            "wage": s.wage
        })
        print(
            f"Период {s.period:3d} | "
            f"Y={s.output:8.2f} | π={s.inflation:6.2%} | u={s.unemployment:6.2%} | "
            f"r={s.interest_rate:6.2%} | w={s.wage:6.2f}"
        )
    return history


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("years", type=int, help="number of years", default=10)
    parser.add_argument("--llm-based-president", action="store_true", help="use LLM for president decisions")
    parser.add_argument("--llm-based-households", action="store_true", help="use LLM for household decisions")
    parser.add_argument("--config", type=str, help="path to config file", default="config.yaml")
    args = parser.parse_args()

    history_yearly = run_simulation(years=args.years, config_path=args.config,
                                    llm_based_president=args.llm_based_president,
                                    llm_based_households=args.llm_based_households)

    plot_all_analytics(history_yearly, output_dir="output")

if __name__ == "__main__":
    main()
