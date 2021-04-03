from enum import Enum

from bonding_curve_simulator.globals import BaseModel
from bonding_curve_simulator.market.growth_curves import CurveConfig


class TaxType(Enum):
    RELATIVE = "relative"
    ABSOLUTE = "absolute"


class TaxConfig(BaseModel):
    tax_amount = 0.0
    tax_type = TaxType.RELATIVE


class WealthConfig(BaseModel):
    supply = 100.0
    reserve = 100.0


class ExchangeConfig(BaseModel):
    bonding_curve_config: CurveConfig = CurveConfig()
    wealth_config: WealthConfig = WealthConfig()
    tax_config: TaxConfig = TaxConfig()
