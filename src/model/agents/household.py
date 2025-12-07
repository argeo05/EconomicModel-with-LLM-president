import json
from dataclasses import dataclass
from typing import Any, List
import perplexity

client = perplexity.Perplexity()


@dataclass
class Household:
    """Consumer agent.

    Attributes:
        income: Income earned
        consumption: Consumption spending
        propensity_to_consume: Marginal propensity to consume
        labor_sensitivity: Labor supply wage sensitivity
        n: Number of identical households
        max_labor_time: Maximum labor time available
        labor_supply: Labor supply quantity
        savings: Accumulated savings
        desired_consumption: Desired consumption amount
        interest_rate_sensitivity: Sensitivity to interest rate in consumption decision
        savings_usage: Proportion of savings used for consumption
    """
    income: float
    consumption: float
    propensity_to_consume: float
    labor_sensitivity: float
    n: int = 1
    max_labor_time: float = 1.0
    labor_supply: float = 0.0
    savings: float = 0.0
    desired_consumption: float = 0.0
    interest_rate_sensitivity: float = 0.5
    savings_usage: float = 0.05

    def decide_labor(self, wage: float) -> float:
        """Decide labor supply based on wage.

        Args:
            wage: Wage rate

        Returns:
            Total labor supply across all households
        """
        raw_labor = self.labor_sensitivity * wage
        self.labor_supply = max(0.0, min(self.max_labor_time, raw_labor))
        return self.labor_supply * self.n

    def update_income(self, wage: float, employment: float) -> None:
        """Update income from employment.

        Args:
            wage: Wage rate
            employment: Employment quantity
        """
        self.income = wage * employment

    def decide_consumption(self, interest_rate: float) -> float:
        """Decide desired consumption.

        Returns:
            Desired consumption amount
        """
        available_funds = self.income + max(0.0, self.savings * self.savings_usage)
        adjusted_propensity = self.propensity_to_consume / (1 + self.interest_rate_sensitivity * interest_rate)
        self.desired_consumption = adjusted_propensity * available_funds
        return self.desired_consumption

    def decide_goods_demand(self, price: float) -> float:
        """Calculate goods demand quantity.

        Args:
            price: Goods price

        Returns:
            Quantity of goods demanded
        """
        if price <= 0:
            return 0.0
        return self.desired_consumption / price

    def update_consumption(self, actual_goods: float, price: float) -> None:
        """Update consumption and savings.

        Args:
            actual_goods: Actual goods purchased
            price: Goods price
        """
        actual_spending = actual_goods * price
        self.consumption = actual_spending
        self.savings += self.income - self.consumption


class Households:
    SAVING_USAGE: float = 0.05
    SYSTEM_MESSAGE = {
        "role": "system",
        "content": """Ты — домохозяйство в симуляции.
                    Я буду присылать тебе данные об экономической ситуации в стране, твоя задача
                    формировать ответ в формате json, при этом ничего кроме json выводить не нужно.
                    Тебе будут предоставлены параметры нескольких домохозяйств, тебе нужно вывести
                    в том же порядке для них значение которое тебя попросят.
                    Стандартное описание это Attributes:
                    income: Income earned
                    consumption: Consumption spending
                    propensity_to_consume: Marginal propensity to consume
                    labor_sensitivity: Labor supply wage sensitivity
                    n: Number of identical households
                    max_labor_time: Maximum labor time available
                    labor_supply: Labor supply quantity
                    savings: Accumulated savings
                    desired_consumption: Desired consumption amount
                    interest_rate_sensitivity: Sensitivity to interest rate in consumption decision
                    Пример(для потребления, для труда аналогично): запрос: домохозяйство 1: income=1000, previous_consumption=800, savings=200, available_funds=1010, домохозяйство 2: income=500, previous_consumption=400, savings=100, available_funds=505
                            вывод: {{"desired_consumptions": [x, y]}}"""
    }

    def __init__(self):
        self.households = []
        self.president_advice: str = None

    def append(self, household: Household) -> None:
        self.households.append(household)

    def _get_advice_from_president(self) -> str:
        if self.president_advice:
            return (f"Президент по прошествию предыдущего периода дал совет{self.president_advice}. "
                    f"Ты не обязан его слушать, но знать о нем должен.")
        else:
            return ""

    def decide_labors(self, wage: float, llm_based: bool) -> List[float]:
        if not llm_based:
            return [h.decide_labor(wage) for h in self.households]

        households_info = ""
        for i, h in enumerate(self.households):
            households_info += (
                f"домохозяйство {i}: "
                f"previous_income={h.income}, "
                f"previous_consumption={h.consumption}, "
                f"max_labor_time={h.max_labor_time}, "
                f"savings={h.savings}, "
            )

        messages = [
            self.SYSTEM_MESSAGE,
            {
                "role": "user",
                "content": f"""Текущая ставка заработной платы: {wage}.
                    Данные по домохозяйствам: {households_info}
                    {self._get_advice_from_president()}
                    Определи для каждого домохозяйства предложение труда
                    то есть количество труда, которое домохозяйство готово предложить при данной зп.
                    Значение должно быть от 0 до max_labor_time для каждого домохозяйства.
                    Ответ в формате(ничего более, далее я паршу это как json): {{"labor_supplies": [число для домохозяйства 0, число для домохозяйства 1, ...]}}"""

            }
        ]

        default_result = [h.decide_labor(wage) for h in self.households]

        for _ in range(5):
            try:
                response = client.chat.completions.create(
                    model="sonar",
                    messages=messages
                ).choices[0].message.content

                data = json.loads(response)
                labor_supplies = data["labor_supplies"]

                for i, h in enumerate(self.households):
                    h.labor_supply = max(0.0, min(h.max_labor_time, float(labor_supplies[i])))

                return [h.labor_supply * h.n for h in self.households]

            except json.decoder.JSONDecodeError as e:
                print(f"LLM returned not right format: {response}, trying again. Exception: {e}")
            except perplexity.APIConnectionError as e:
                print("Network connection failed")
                print(e.__cause__)
            except perplexity.RateLimitError as e:
                print("Rate limit exceeded, please retry later")
            except perplexity.APIStatusError as e:
                print(f"API error: {e.status_code}")
                print(e.response)

        return default_result

    def decide_consumptions(self, interest_rate: float, llm_based: bool) -> None:
        if not llm_based:
            for h in self.households:
                h.decide_consumption(interest_rate)
            return

        households_info = ""
        for i, h in enumerate(self.households):
            available_funds = h.income + max(0.0, h.savings * h.savings_usage)
            households_info += (
                f"домохозяйство {i}: "
                f"income={h.income}, "
                f"previous_consumption={h.consumption}"
                f"savings={h.savings}"
                f"available_funds={available_funds}, "
            )

        messages = [
            self.SYSTEM_MESSAGE,
            {
                "role": "user",
                "content": f"""Текущая процентная ставка: {interest_rate}.
                    Данные по домохозяйствам: {households_info}
                    {self._get_advice_from_president()}
                    Определи для каждого домохозяйства желаемое потребление 
                    то есть сколько денег домохозяйство хочет потратить на товары. Не больше чем available_funds.
                    Ответ в формате(ничего более, далее я паршу это как json): {{"desired_consumptions": [число для домохозяйства 0, число для домохозяйства 1, ...]}}
                    """
            }
        ]

        for _ in range(5):
            try:
                response = client.chat.completions.create(
                    model="sonar",
                    messages=messages
                ).choices[0].message.content

                data = json.loads(response)
                desired_consumptions = data["desired_consumptions"]

                for i, h in enumerate(self.households):
                    available_funds = h.income + h.savings
                    h.desired_consumption = max(0.0, min(available_funds, float(desired_consumptions[i])))

            except json.decoder.JSONDecodeError as e:
                print(f"LLM returned not right format: {response}, trying again. Exception: {e}")
            except perplexity.APIConnectionError as e:
                print("Network connection failed")
                print(e.__cause__)
            except perplexity.RateLimitError as e:
                print("Rate limit exceeded, please retry later")
            except perplexity.APIStatusError as e:
                print(f"API error: {e.status_code}")
                print(e.response)
