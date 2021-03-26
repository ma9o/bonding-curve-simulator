from bonding_curve_simulator.mesa.agents.trader import TraderAgent
from typing import Dict
from bonding_curve_simulator.mesa.agents.creator import CreatorAgent
from bonding_curve_simulator.market.bonding_curve import BondingCurve
from enum import Enum


class TaxType(Enum):
    RELATIVE = 0
    ABSOLUTE = 1


class Exchange:
    def __init__(
        self,
        bonding_curve: BondingCurve,
        config: Dict = {
            "supply": 100,
            "reserve": 100,
            "tax_amount": 0.0,
            "tax_type": TaxType.RELATIVE,
        },
    ):
        self.bonding_curve = bonding_curve

        self.supply = config["supply"]
        self.reserve = config["reserve"]
        self.tax_amount = config["tax_amount"]
        self.tax_type = config["tax_type"]

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
        self.creator.wealth += tax

        # Perform transaction
        effective_amount = reserve_amount - tax

        trader.reserve -= effective_amount
        trader.supply += self.bonding_curve.get_purchase_return(
            self.supply, effective_amount
        )

    def sell(self, trader: TraderAgent, supply_amount) -> None:
        trader.supply -= supply_amount
        trader.reserve += self.bonding_curve.get_sale_return(self.supply, supply_amount)
