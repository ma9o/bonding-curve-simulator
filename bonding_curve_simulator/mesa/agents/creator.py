from typing import cast
from mesa import Agent


class CreatorAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.wealth = 1
        self.monthly_revenue = 100

    def step(self):
        pass
        # print(repr(self.model.schedule))
        # cast(SimulationModel, self.model).exchange.reserve += self.monthly_revenue
