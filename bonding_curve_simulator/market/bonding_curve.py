from dataclasses import dataclass
from enum import Enum
from typing import Dict, Tuple, Union
import scipy.integrate as integrate
from scipy.optimize import fsolve
import numpy as np


class CurveType(Enum):
    POWER = "power"
    LOGISTIC = "logistic"


@dataclass
class LogisticConfig:
    x: float = 0


@dataclass
class PowerConfig:
    m: float = 1.0 / 400
    n: float = 2.0


class BondingCurve:
    def __init__(self, config: Union[LogisticConfig, PowerConfig]):

        # TODO: parametrize -> https://en.wikipedia.org/wiki/Generalised_logistic_function
        if isinstance(config, LogisticConfig):
            self.bonding_formula = lambda x: 1.0 / ((1.0 - np.exp(1)) ** (-x))

        if isinstance(config, PowerConfig):
            self.bonding_formula = lambda x: config.m * (x ** config.n)

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
