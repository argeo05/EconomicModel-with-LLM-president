import matplotlib.pyplot as plt


class Plots:
    """Interactive plots for macroeconomic indicators.

    Attributes:
        fig: Matplotlib figure
        axes: Subplot axes array
        lines: Dictionary of plot lines
        periods: List of period numbers
        output_data: Output history
        inflation_data: Inflation history
        unemployment_data: Unemployment history
        interest_rate_data: Interest rate history
        wage_data: Wage history
        president_messages: Recent president messages
    """
    
    def __init__(self):
        self.fig = None
        self.axes = None
        self.lines = {}
        self.periods = []
        self.output_data = []
        self.inflation_data = []
        self.unemployment_data = []
        self.interest_rate_data = []
        self.wage_data = []
        self.president_messages = []

        plt.ion()
        plt.show(block=False)
        self.init_macroeconomic_plots()

    def init_macroeconomic_plots(self) -> None:
        """Initialize subplot layout and styling."""
        self.fig, self.axes = plt.subplots(2, 3, figsize=(15, 8))
        self.fig.suptitle('Макроэкономические показатели', fontsize=16, fontweight='bold')

        self.lines = {
            'output': self.axes[0, 0].plot([], [], color='#2E86AB', linewidth=2)[0],
            'inflation': self.axes[0, 1].plot([], [], color='#A23B72', linewidth=2)[0],
            'unemployment': self.axes[0, 2].plot([], [], color='#F18F01', linewidth=2)[0],
            'interest_rate': self.axes[1, 0].plot([], [], color='#C73E1D', linewidth=2)[0],
            'wage': self.axes[1, 1].plot([], [], color='#6A994E', linewidth=2)[0],
            'output_gap': self.axes[1, 2].plot([], [], color='#BC4B51', linewidth=2)[0]
        }

        self.axes[0, 0].set_title('Выпуск (Y)', fontweight='bold')
        self.axes[0, 0].set_xlabel('Период')
        self.axes[0, 0].set_ylabel('Y')
        self.axes[0, 0].grid(True, alpha=0.3)
        self.axes[0, 0].axhline(y=240, color='red', linestyle='--', alpha=0.5, label='Y*')
        self.axes[0, 0].legend()

        self.axes[0, 1].set_title('Инфляция (п)', fontweight='bold')
        self.axes[0, 1].set_xlabel('Период')
        self.axes[0, 1].set_ylabel('п (%)')
        self.axes[0, 1].grid(True, alpha=0.3)
        self.axes[0, 1].axhline(y=2, color='red', linestyle='--', alpha=0.5, label='п*')
        self.axes[0, 1].legend()

        self.axes[0, 2].set_title('Безработица (u)', fontweight='bold')
        self.axes[0, 2].set_xlabel('Период')
        self.axes[0, 2].set_ylabel('u (%)')
        self.axes[0, 2].grid(True, alpha=0.3)

        self.axes[1, 0].set_title('Процентная ставка (r)', fontweight='bold')
        self.axes[1, 0].set_xlabel('Период')
        self.axes[1, 0].set_ylabel('r (%)')
        self.axes[1, 0].grid(True, alpha=0.3)
        self.axes[1, 0].axhline(y=3, color='red', linestyle='--', alpha=0.5, label='r*')
        self.axes[1, 0].legend()

        self.axes[1, 1].set_title('Зарплата (w)', fontweight='bold')
        self.axes[1, 1].set_xlabel('Период')
        self.axes[1, 1].set_ylabel('w')
        self.axes[1, 1].grid(True, alpha=0.3)

        self.axes[1, 2].set_title('Президент сказал:', fontweight='bold')

        plt.tight_layout()

    def update(self, period: int, output: float, inflation: float, unemployment: float,
               rate: float, wage: float, president_message: str = "") -> None:
        """Update plots with new data point.

        Args:
            period: Current period number
            output: Output value
            inflation: Inflation rate
            unemployment: Unemployment rate
            rate: Interest rate
            wage: Wage rate
            president_message: President message to display
        """
        self.periods.append(period)
        self.output_data.append(output)
        self.inflation_data.append(inflation * 100)
        self.unemployment_data.append(unemployment * 100)
        self.interest_rate_data.append(rate * 100)
        self.wage_data.append(wage)
        if president_message:
            self.president_messages.append(president_message)
            if len(self.president_messages) > 3:
                self.president_messages = self.president_messages[-3:]

        self.lines['output'].set_data(self.periods, self.output_data)
        self.lines['inflation'].set_data(self.periods, self.inflation_data)
        self.lines['unemployment'].set_data(self.periods, self.unemployment_data)
        self.lines['interest_rate'].set_data(self.periods, self.interest_rate_data)
        self.lines['wage'].set_data(self.periods, self.wage_data)

        for ax in self.axes.flat:
            ax.relim()
            ax.autoscale_view()

        ax_president = self.axes[1, 2]
        ax_president.clear()
        ax_president.set_title('Президент сказал:', fontweight='bold')
        ax_president.axis('off')
        y_positions = [0.85, 0.55, 0.25]
        font_size = 10
        max_chars = 90
        for i, msg in enumerate(self.president_messages):
            message = f"{period - len(self.president_messages) + 1 + i}. {msg}"
            if len(message) > max_chars:
                message = '\n'.join([message[j:j+max_chars] for j in range(0, len(message), max_chars)])
            ax_president.text(0.01, y_positions[i], message, fontsize=font_size, va='top', ha='left', wrap=True,
                              color="black", transform=ax_president.transAxes)

        self.fig.tight_layout()
        self.fig.canvas.draw_idle()
        self.fig.canvas.flush_events()

    def show(self) -> None:
        """Show plots in blocking mode."""
        plt.show(block=True)
