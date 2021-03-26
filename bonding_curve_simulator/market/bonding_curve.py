from decimal import *
from enum import Enum
from typing import Dict, Tuple
import scipy.integrate as integrate
from scipy.optimize import fsolve
import numpy as np


class CurveType(Enum):
    POWER = 0
    LOGISTIC = 1


class BondingCurve:
    def __init__(
        self,
        curve_type: CurveType = CurveType.POWER,
        config: Dict = {"m": 1 / 400, "n": 2.0},
    ):
        # TODO: parametrize -> https://en.wikipedia.org/wiki/Generalised_logistic_function
        if curve_type == CurveType.LOGISTIC:
            self.bonding_formula = lambda x: 1.0 / ((1.0 - np.exp(1)) ** (-x))

        if curve_type == CurveType.POWER:
            self.bonding_formula = lambda x: config["m"] * (x ** config["n"])

    def current_price(self, supply) -> float:
        return self.bonding_formula(supply)

    # Integrate curve: supply -> (supply - sale_amount)
    def get_sale_return(self, supply: float, sale_amount: float) -> float:
        y, abserr = integrate.quad(self.bonding_formula, supply, supply - sale_amount)
        return abs(y)

    # Solve integral: supply -> (supply + x) = purchase_cost, return difference
    def get_purchase_return(self, supply: float, purchase_cost: float) -> float:
        x, info, ier, msg = fsolve(
            lambda x: purchase_cost - integrate.quad(self.bonding_formula, supply, x),
            supply,
        )

        if ier == 1:
            return x - supply
        else:
            raise (msg)
