from bonding_curve_simulator.market.growth_curves import CurveConfig
from pydantic.main import BaseModel
from enum import Enum


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
