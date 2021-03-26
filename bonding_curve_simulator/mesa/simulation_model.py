from bonding_curve_simulator.market.bonding_curve import BondingCurve
from typing import Dict
from bonding_curve_simulator.market.exchange import Exchange
from bonding_curve_simulator.mesa.agents.creator import CreatorAgent
from bonding_curve_simulator.mesa.agents.trader import TraderAgent
from mesa import Model
from mesa.time import RandomActivation


class SimulationModel(Model):
    def __init__(self, exchange: Exchange, max_steps=1000, num_agents=1000):
        self.result = []
        self.max_steps = max_steps
        self.num_agents = num_agents

        self.schedule = RandomActivation(self)

        creator_agent = CreatorAgent(0, self)

        self.schedule.add(creator_agent)

        self.exchange = exchange

        self.exchange.set_creator(creator_agent)

        for i in range(1, self.num_agents):
            a = TraderAgent(i, self)
            self.schedule.add(a)

    def step(self):
        if self.schedule.steps < self.max_steps:
            self.running = False
        else:
            self.schedule.step()