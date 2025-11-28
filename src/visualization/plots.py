import matplotlib.pyplot as plt
from typing import List, Dict
import numpy as np


def plot_macroeconomic_indicators(history: List[Dict[str, float]], save_path: str = None) -> None:
    """Plot macroeconomic indicators over time.

    Args:
        history: List of economic state dictionaries
        save_path: Optional path to save figure
    """
    periods = [h["period"] for h in history]
    output = [h["output"] for h in history]
    inflation = [h["inflation"] * 100 for h in history]
    unemployment = [h["unemployment"] * 100 for h in history]
    interest_rate = [h["rate"] * 100 for h in history]
    wage = [h["wage"] for h in history]

    fig, axes = plt.subplots(2, 3, figsize=(15, 8))
    fig.suptitle('Макроэкономические показатели', fontsize=16, fontweight='bold')

    axes[0, 0].plot(periods, output, color='#2E86AB', linewidth=2)
    axes[0, 0].set_title('Выпуск (Y)', fontweight='bold')
    axes[0, 0].set_xlabel('Период')
    axes[0, 0].set_ylabel('Y')
    axes[0, 0].grid(True, alpha=0.3)
    axes[0, 0].axhline(y=240, color='red', linestyle='--', alpha=0.5, label='Y*')
    axes[0, 0].legend()

    axes[0, 1].plot(periods, inflation, color='#A23B72', linewidth=2)
    axes[0, 1].set_title('Инфляция (п)', fontweight='bold')
    axes[0, 1].set_xlabel('Период')
    axes[0, 1].set_ylabel('п (%)')
    axes[0, 1].grid(True, alpha=0.3)
    axes[0, 1].axhline(y=2, color='red', linestyle='--', alpha=0.5, label='п*')
    axes[0, 1].legend()

    axes[0, 2].plot(periods, unemployment, color='#F18F01', linewidth=2)
    axes[0, 2].set_title('Безработица (u)', fontweight='bold')
    axes[0, 2].set_xlabel('Период')
    axes[0, 2].set_ylabel('u (%)')
    axes[0, 2].grid(True, alpha=0.3)

    axes[1, 0].plot(periods, interest_rate, color='#C73E1D', linewidth=2)
    axes[1, 0].set_title('Процентная ставка (r)', fontweight='bold')
    axes[1, 0].set_xlabel('Период')
    axes[1, 0].set_ylabel('r (%)')
    axes[1, 0].grid(True, alpha=0.3)
    axes[1, 0].axhline(y=3, color='red', linestyle='--', alpha=0.5, label='r*')
    axes[1, 0].legend()

    axes[1, 1].plot(periods, wage, color='#6A994E', linewidth=2)
    axes[1, 1].set_title('Зарплата (w)', fontweight='bold')
    axes[1, 1].set_xlabel('Период')
    axes[1, 1].set_ylabel('w')
    axes[1, 1].grid(True, alpha=0.3)

    output_gap = [(y - 240) / 240 * 100 for y in output]
    axes[1, 2].plot(periods, output_gap, color='#BC4B51', linewidth=2)
    axes[1, 2].set_title('Разрыв выпуска', fontweight='bold')
    axes[1, 2].set_xlabel('Период')
    axes[1, 2].set_ylabel('(Y - Y*)/Y* (%)')
    axes[1, 2].grid(True, alpha=0.3)
    axes[1, 2].axhline(y=0, color='red', linestyle='--', alpha=0.5)

    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"График сохранён: {save_path}")
    
    plt.show()

# TODO: МБ реализовать визуализацию кривой Филлипса и Тейлора

def plot_all_analytics(history: List[Dict[str, float]], output_dir: str = "outputs") -> None:
    """Generate all analytical plots.

    Args:
        history: List of economic state dictionaries
        output_dir: Directory to save plots
    """
    import os
    os.makedirs(output_dir, exist_ok=True)

    print("\nСоздание аналитических графиков...")

    plot_macroeconomic_indicators(history, save_path=f"{output_dir}/macroeconomic_indicators.png")

    print(f"\nВсе графики сохранены в папку: {output_dir}/")
