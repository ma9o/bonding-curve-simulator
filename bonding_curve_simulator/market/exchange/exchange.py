from bonding_curve_simulator.market.bonding_curve import BondingCurve
from bonding_curve_simulator.market.exchange.types import ExchangeConfig, TaxType
from bonding_curve_simulator.mesa.agent.creator import CreatorAgent
from bonding_curve_simulator.mesa.agent.trader import TraderAgent


class Exchange:
    def __init__(self, config: ExchangeConfig = ExchangeConfig()):
        self.supply = config.wealth_config.supply
        self.reserve = config.wealth_config.reserve
        self.tax_amount = config.tax_config.tax_amount
        self.tax_type = config.tax_config.tax_type
        self.bonding_curve = BondingCurve(config.bonding_curve_config)

    def set_creator(self, creator: CreatorAgent):
        self.creator = creator

    def __transact__(self, trader: TraderAgent, supply, reserve):
        self.supply += supply
        trader.supply += supply

        self.reserve += reserve
        trader.reserve -= reserve

    def __get_tax_amount__(self, reserve_amount) -> float:
        tax = 0
        if self.tax_type == TaxType.ABSOLUTE:
            if reserve_amount <= self.tax_amount:
                return 0
            else:
                tax = self.tax_amount
        elif self.tax_type == TaxType.RELATIVE:
            tax = reserve_amount * self.tax_amount

        return tax

    def buy(self, trader: TraderAgent, reserve_amount) -> None:
        reserve_amount = min(reserve_amount, self.reserve)

        if reserve_amount <= 0:
            return

        tax = self.__get_tax_amount__(reserve_amount)

        supply_amount = self.bonding_curve.get_purchase_return(
            self.supply, reserve_amount - tax
        )

        if self.supply - supply_amount > 0:
            self.creator.reserve += tax
            reserve_amount -= tax
            self.__transact__(trader, supply_amount, reserve_amount)

    def sell(self, trader: TraderAgent, supply_amount) -> None:
        supply_amount = min(supply_amount, self.supply)

        if supply_amount <= 0:
            return

        reserve_amount = self.bonding_curve.get_sale_return(self.supply, supply_amount)

        if self.reserve - reserve_amount > 0:
            self.__transact__(trader, -supply_amount, -reserve_amount)

    def current_price(self) -> float:
        return self.bonding_curve.current_price(self.supply)
