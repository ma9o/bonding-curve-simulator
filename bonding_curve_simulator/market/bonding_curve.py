from bonding_curve_simulator.market.growth_curves import (
    ExponentialConfig,
    LogisticConfig,
    exponential,
    logistic,
)
from typing import Dict, Tuple, Union
import scipy.integrate as integrate
from scipy.optimize import fsolve
import numpy as np


class BondingCurve:
    def __init__(self, config: Union[LogisticConfig, ExponentialConfig]):

        if isinstance(config, LogisticConfig):
            self.bonding_formula = logistic(config)

        if isinstance(config, ExponentialConfig):
            self.bonding_formula = exponential(config)

    def current_price(self, supply) -> float:
        return self.bonding_formula(supply)

    # Integrate curve: supply -> (supply - sale_amount)
    def get_sale_return(self, supply: float, sale_amount: float) -> float:
        y, abserr = integrate.quad(self.bonding_formula, supply, supply - sale_amount)
        return abs(y)

    # Solve integral: supply -> (supply + x) = purchase_cost, return difference
    def get_purchase_return(self, supply: float, purchase_cost: float) -> float:
        # TODO: bottleneck
        x, info, ier, msg = fsolve(
            lambda x: purchase_cost
            - integrate.quad(self.bonding_formula, supply, x)[0],
            supply,
            full_output=True,
        )

        if ier == 1:
            return x[0] - supply
        else:
            raise (msg)
