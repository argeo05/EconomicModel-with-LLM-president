from dataclasses import dataclass


@dataclass
class CentralBank:
    """Monetary policy institution.

    Attributes:
        r: Current interest rate
        r_star: Natural interest rate
        pi_star: Target inflation rate
        Y_star: Potential output
        phi_pi: Inflation response coefficient
        phi_y: Output gap response coefficient
        r_min: Minimum interest rate
        r_max: Maximum interest rate
        adjustment_speed: Rate adjustment speed
    """
    r: float
    r_star: float
    pi_star: float
    Y_star: float
    phi_pi: float
    phi_y: float
    r_min: float = 0.0
    r_max: float = 0.10
    adjustment_speed: float = 0.3 

    def propose_rate(self, inflation: float, output: float) -> float:
        """Calculate interest rate using Taylor rule.

        Args:
            inflation: Current inflation rate
            output: Current output

        Returns:
            New interest rate
        """
        output_gap = (output - self.Y_star) / max(self.Y_star, 1e-6)
        target_rate = self.r_star + self.phi_pi * (inflation - self.pi_star) + self.phi_y * output_gap
        self.r += self.adjustment_speed * (target_rate - self.r)
        self.r = min(max(self.r, self.r_min), self.r_max)
        return self.r
