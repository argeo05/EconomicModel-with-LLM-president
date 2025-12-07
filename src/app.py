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
from .visualization import DataEconomyHandler
from .model.agents import Households, President

DEFAULT_PRESIDENT_SETUP = "Главная цель — рост ВВП. Ты любишь большие цифры, поэтому маленькая ставка тебя не устраивает."


def run_simulation(years: int, config_path: str, llm_based_president: bool,
                   llm_based_households: bool, president_setup: str, show_plots: bool = True) -> DataEconomyHandler:
    """Run economic simulation.

    Args:
        years: Number of simulation periods
        config_path: Path to configuration file
        llm_based_president: If True use LLM for president decisions
        llm_based_households: If True use LLM for household decisions
        president_setup: Character setup for president LLM
        show_plots: If True display interactive plots

    Returns:
        DataEconomyHandler with simulation results
    """
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
    president = President(president_setup)
    history = []
    if show_plots:
        plots = Plots()

    economy = Economy(
        households=households,
        firms=firms,
        central_bank=cb,
        president=president,
        labor_market=labor_market,
        goods_market=goods_market,
        state=EconomyState.initial(initial_state),
        llm_based_president=llm_based_president,
        llm_based_households=llm_based_households,
    )

    for _ in range(years):
        economy.step()
        s = economy.state
        president_advice = s.president_message
        history.append((s.output, s.inflation, s.unemployment, s.interest_rate, s.wage,
                        president_advice))
        if show_plots:
            plots.update(s.period, s.output, s.inflation, s.unemployment, s.interest_rate, s.wage,
                         president_advice)
        print(
            f"Период {s.period:3d} | "
            f"Y={s.output:8.2f} | π={s.inflation:6.2%} | u={s.unemployment:6.2%} | "
            f"r={s.interest_rate:6.2%} | w={s.wage:6.2f}"
        )

    data_base.append_all(history)
    if show_plots:
        plots.show()
    return data_base


def main() -> None:
    """Main entry point for simulation."""
    parser = argparse.ArgumentParser()
    parser.add_argument("years", type=int, help="number of years", default=10)
    parser.add_argument("--llm-based-president", "-pr", action="store_true", help="use LLM for president decisions")
    parser.add_argument("--president-setup", "-ps", type=str, help="message to llm president",
                        default=DEFAULT_PRESIDENT_SETUP)
    parser.add_argument("--disable-plots", action="store_true", help="Disable plots")
    parser.add_argument("--llm-based-households", "-hh", action="store_true", help="use LLM for household decisions")
    parser.add_argument("--config", type=str, help="path to config file", default="config.yaml")
    parser.add_argument("--profiling", action="store_true", help="Enable profiling")
    args = parser.parse_args()

    if args.profiling:
        import cProfile
        cProfile.run(f"""run_simulation(years={args.years}, config_path="{args.config}",
                       llm_based_president={args.llm_based_president},
                       llm_based_households={args.llm_based_households},
                       president_setup="{args.president_setup}",
                       show_plots={not args.disable_plots})""", filename="profile_new.prof")
    else:
        run_simulation(years=args.years, config_path=args.config,
                       llm_based_president=args.llm_based_president,
                       president_setup=args.president_setup,
                       llm_based_households = args.llm_based_households,
                       show_plots=not args.disable_plots)

if __name__ == "__main__":
    main()
