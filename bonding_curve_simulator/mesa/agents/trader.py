from bonding_curve_simulator.mesa.simulation_model import SimulationModel
from typing import cast
from mesa import Agent


class TraderAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.supply = 0.0
        self.reserve = 10.0

    def step(self):
        # The agent's step will go here.
        r = self.random.randint(0, 100)

        if r >= 25 and r <= 75:
            pass
        elif r < 25:
            sale_amount = self.model.random.uniform(0.0, self.supply)
            cast(SimulationModel, self.model).exchange.sell(self, sale_amount)
        elif r > 75:
            reserve_amount = self.model.random.uniform(0.0, self.reserve)
            cast(SimulationModel, self.model).exchange.buy(self, reserve_amount)
