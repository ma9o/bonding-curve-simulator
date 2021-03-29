from dataclasses import dataclass
from enum import Enum
from typing import Dict, Tuple, Union
import scipy.integrate as integrate
from scipy.optimize import fsolve
import numpy as np


class CurveType(Enum):
    EXPONENTIAL = "exponential"
    LOGISTIC = "logistic"


# https://en.wikipedia.org/wiki/Generalised_logistic_function
@dataclass
class LogisticConfig:
    a: float = 0.0
    k: float = 1.0
    b: float = 3.0
    v: float = 0.5
    q: float = 0.5
    c: float = 1.0
    m: float = 3.0


@dataclass
class ExponentialConfig:
    m: float = 1.0 / 400
    n: float = 2.0
    y0: float = 0.0
    x0: float = 0.0


class BondingCurve:
    def __init__(self, config: Union[LogisticConfig, ExponentialConfig]):

        if isinstance(config, LogisticConfig):
            self.bonding_formula = lambda x: config.a + (
                (config.k - config.a)
                / (config.c + ((config.q * np.e) ** (-config.b * (x - config.m))))
                ** (1 / config.v)
            )

        if isinstance(config, ExponentialConfig):
            self.bonding_formula = lambda x: config.y0 + config.m * (
                (x - config.x0) ** config.n
            )

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
