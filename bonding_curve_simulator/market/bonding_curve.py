import scipy.integrate as integrate
from scipy.optimize import fsolve
from bonding_curve_simulator.market.growth_curves import (
    CurveConfig,
    curve_type_function,
)


class BondingCurve:
    def __init__(self, config: CurveConfig = CurveConfig()):
        self.bonding_formula = curve_type_function[config.curve_type](
            config.curve_params
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
