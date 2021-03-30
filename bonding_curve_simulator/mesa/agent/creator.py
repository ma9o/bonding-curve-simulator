from bonding_curve_simulator.market.exchange import WealthConfig
from typing import Callable
from mesa import Agent


class CreatorAgent(Agent):
    def __init__(
        self,
        unique_id,
        model,
        wealth_config: WealthConfig,
        growth_curve: Callable[[float], float],
    ):
        super().__init__(unique_id, model)
        self.reserve = wealth_config.reserve
        self.supply = wealth_config.supply
        self.growth_curve = growth_curve

    def step(self):
        steps = self.model.schedule.steps

        if steps % 30 == 0:
            self.model.exchange.reserve += self.growth_curve(steps)
