from bonding_curve_simulator.market.exchange.types import ExchangeConfig, TaxType
from bonding_curve_simulator.market.bonding_curve import BondingCurve
from bonding_curve_simulator.mesa.agent.trader import TraderAgent
from bonding_curve_simulator.mesa.agent.creator import CreatorAgent


class Exchange:
    def __init__(self, config: ExchangeConfig = ExchangeConfig()):
        self.supply = config.wealth_config.supply
        self.reserve = config.wealth_config.reserve
        self.tax_amount = config.tax_config.tax_amount
        self.tax_type = config.tax_config.tax_type
        self.bonding_curve = BondingCurve(config.bonding_curve_config)

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
