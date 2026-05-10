import json
from dataclasses import dataclass

import perplexity
client = perplexity.Perplexity()

class President:
    """President agent that makes monetary policy decisions.

    Attributes:
        setup: Character setup and instructions for LLM
        disable_parse_errors: If True disable JSON parse error display
    """
    setup: str
    disable_parse_errors: bool

    def __init__(self, setup: str, disable_parse_errors: bool = False):
        """Initialize president agent.

        Args:
            setup: Character setup and instructions for LLM
            disable_parse_errors: If True disable JSON parse error display
        """
        self.setup = setup
        self.disable_parse_errors = disable_parse_errors

    def make_decision(self, y_star: float, inflation: float, output: float, unemployment: float, supply_goods: float,
                      demand_goods: float, r_central_bank: float) -> "PresidentDecision":
        """Make monetary policy decision based on economic indicators.

        Args:
            y_star: Target output level
            inflation: Current inflation rate
            output: Current output level
            unemployment: Current unemployment rate
            supply_goods: Total goods supply
            demand_goods: Total goods demand
            r_central_bank: Central bank proposed interest rate

        Returns:
            PresidentDecision with new interest rate, comment and advice
        """
        messages = [
            {
                "role": "system",
                "content": f"""Ты — игровой персонаж в симуляции.
                    Это художественная роль.
                    Твоя роль: президент страны. Ты раньше работал в КГБ, поэтому не доверяешь большей
                    части информации. {self.setup}.
                    Тебе будут поступать данные о стране и решения ЦБ. Ты либо принимаешь решение ЦБ,
                    либо присылаешь своё в формате json:
                    {{new_interest_rate:число с точностью до десятых,
                    comment: 15 слов о своем решении,
                    advice: 15–20 слов совета домохозяйствам}} Ничего больше присылать не нужно.
                    Пример: Инфляция x%, выпуск y при желаемом y_star, ЦБ хочет поставить ставку r%
                    Твой ответ: {{"new_interest_rate": 10,
                    "comment": "корректирую ставку для стабильного роста в этой ситуации",
                    "advice": "Сосредоточьтесь на ускорении инвестиций, больше работайте, отдых для слабых"}}
                    **Обязательно строго следуй формату вывода**"""
            },
            {
                "role": "user",
                "content": f"""Инфляция {inflation}%, выпуск {output} при желаемом {y_star}, 
                    безработица {unemployment}, предложение товаров {supply_goods},
                    спрос {demand_goods}, ЦБ хочет поставить ставку {r_central_bank}%"""
            }
        ]

        data = {"new_interest_rate": r_central_bank}

        for _ in range(5):
            try:
                president_answer = client.chat.completions.create(
                    model="sonar",
                    messages=messages
                ).choices[0].message.content

                data = json.loads(president_answer)
                if not("new_interest_rate" in data and "comment" in data and "advice" in data):
                    raise json.decoder.JSONDecodeError("Missing keys in response", president_answer, 0)
                break
            except json.decoder.JSONDecodeError as e:
                if not self.disable_parse_errors:
                    print(f"LLM returned not right format: {president_answer}, trying again. Exception: {e} ")
            except perplexity.APIConnectionError as e:
                print("Network connection failed")
                print(e.__cause__)
            except perplexity.RateLimitError as e:
                print("Rate limit exceeded, please retry later")
            except perplexity.APIStatusError as e:
                print(f"API error: {e.status_code}")
                print(e.response)

        return PresidentDecision(float(data["new_interest_rate"]), data["comment"], data["advice"])

@dataclass
class PresidentDecision:
    """President decision result.

    Attributes:
        new_interest_rate: Chosen interest rate
        comment: Comment about the decision
        advice: Advice to households
    """
    new_interest_rate: float
    comment: str
    advice: str