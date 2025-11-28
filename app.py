import matplotlib.pyplot as plt
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


def run_simulation(periods_per_year: int, years: int, config_path: str) -> list[dict[str, float]]:
    config = load_config(config_path)
    total_periods = periods_per_year * years

    households = []
    for class_name in ["high_income", "middle_income", "low_income"]:
        class_config = config["households"][class_name]
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
    for firm_type in ["large", "medium", "small"]:
        firm_config = config["firms"][firm_type]
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
        state=EconomyState.initial(initial_state)
    )

    history = []
    for _ in range(total_periods):
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
    years = 30
    print("\nСценарий 1: обновление экономики раз в год")
    history_yearly = run_simulation(periods_per_year=1, years=years, config_path="config.yaml")
    
    plot_all_analytics(history_yearly, output_dir="outputs")
if __name__ == "__main__":
    main()
