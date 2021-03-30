from bonding_curve_simulator.market.exchange import Exchange
from bonding_curve_simulator.mesa.agents.creator import CreatorAgent
from bonding_curve_simulator.mesa.agents.trader import TraderAgent
from mesa import Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector


class SimulationModel(Model):
    def __init__(
        self, exchange: Exchange, max_steps=3650, num_agents=100, max_revenue=100.0
    ):
        super().__init__()

        self.max_steps = max_steps
        self.num_agents = num_agents

        self.schedule = RandomActivation(self)

        creator_agent = CreatorAgent(0, self, max_revenue)

        self.schedule.add(creator_agent)

        self.exchange = exchange

        self.exchange.set_creator(creator_agent)

        for i in range(1, self.num_agents):
            a = TraderAgent(i, self)
            self.schedule.add(a)

        self.datacollector = DataCollector(
            model_reporters={
                "Price": self.exchange.current_price,
                "Supply": lambda x: self.exchange.supply,
                "Reserve": lambda x: self.exchange.reserve,
            },
            agent_reporters={"Supply": "supply", "Reserve": "reserve"},
        )

    def step(self):
        self.datacollector.collect(self)

        if self.schedule.steps > self.max_steps:
            self.running = False
        else:
            self.schedule.step()