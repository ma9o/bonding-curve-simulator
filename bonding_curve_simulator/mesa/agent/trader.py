from bonding_curve_simulator.market.exchange import WealthConfig
from mesa import Agent


class TraderAgent(Agent):
    def __init__(self, unique_id, model, wealth_config: WealthConfig, trading_strategy):
        super().__init__(unique_id, model)
        self.supply = wealth_config.supply
        self.reserve = wealth_config.reserve
        self.trading_strategy = trading_strategy

    def step(self):
        self.trading_strategy(self)
