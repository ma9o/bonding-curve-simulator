from bonding_curve_simulator.mesa.agents.trader import TraderAgent
from typing import Dict
from bonding_curve_simulator.mesa.agents.creator import CreatorAgent
from bonding_curve_simulator.market.bonding_curve import BondingCurve
from enum import Enum
from dataclasses import dataclass


class TaxType(Enum):
    RELATIVE = "relative"
    ABSOLUTE = "absolute"


@dataclass
class TaxConfig:
    tax_amount: float = 0.0
    tax_type: TaxType = TaxType.RELATIVE


@dataclass
class WealthConfig:
    supply: float = 100.0
    reserve: float = 100.0


class Exchange:
    def __init__(
        self,
        bonding_curve: BondingCurve,
        exchange_config: WealthConfig = WealthConfig(),
        tax_config: TaxConfig = TaxConfig(),
    ):
        self.bonding_curve = bonding_curve

        self.supply = exchange_config.supply
        self.reserve = exchange_config.reserve
        self.tax_amount = tax_config.tax_amount
        self.tax_type = tax_config.tax_type

    def set_creator(self, creator: CreatorAgent):
        self.creator = creator

    def buy(self, trader: TraderAgent, reserve_amount) -> None:

        # Apply tax to transaction
        tax = None
        if self.tax_type == TaxType.ABSOLUTE:
            if reserve_amount <= self.tax_amount:
                return
            else:
                tax = self.tax_amount
        elif self.tax_type == TaxType.RELATIVE:
            tax = reserve_amount * self.tax_amount

        # Send tax to creator
        self.creator.reserve += tax

        # Perform transaction
        reserve_amount -= tax
        supply_amount = self.bonding_curve.get_purchase_return(
            self.supply, reserve_amount
        )

        trader.reserve -= reserve_amount
        trader.supply += supply_amount

        self.reserve += reserve_amount
        self.supply -= supply_amount

    def sell(self, trader: TraderAgent, supply_amount) -> None:
        reserve_amount = self.bonding_curve.get_sale_return(self.supply, supply_amount)

        trader.supply -= supply_amount
        trader.reserve += reserve_amount

        self.supply += supply_amount
        self.reserve -= reserve_amount

    def current_price(self) -> float:
        return self.bonding_curve.current_price(self.supply)
