from enum import Enum
from mesa import Agent


class CratorType(Enum):
    SUCCESSFUL = 0
    AVERAGE = 1
    UNSUCCESSFUL = 2


class CreatorAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.reserve = 1
        self.supply = 0
        self.monthly_revenue = 10

    def step(self):
        if self.model.schedule.steps % 30 == 0:
            self.model.exchange.reserve += self.monthly_revenue
