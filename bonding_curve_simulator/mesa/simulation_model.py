import uuid
from math import floor
from typing import Callable, List, Tuple

from mesa import Model
from mesa.datacollection import DataCollector
from mesa.time import RandomActivation
from progress.bar import Bar

from bonding_curve_simulator.globals import BaseModel
from bonding_curve_simulator.market.exchange.exchange import Exchange
from bonding_curve_simulator.market.growth_curves import (
    CurveConfig,
    curve_type_function,
)
from bonding_curve_simulator.mesa.agent.creator import CreatorAgent, CreatorAgentConfig
from bonding_curve_simulator.mesa.agent.trader import TraderAgent, TraderAgentConfig


class TraderAgentsConfig(BaseModel):
    curve_config: CurveConfig = CurveConfig()
    agent_config: TraderAgentConfig = TraderAgentConfig()


class SimulationModelConfig(BaseModel):
    max_steps: int = 365 * 10
    agents: List[TraderAgentsConfig] = [TraderAgentsConfig()]
    creator: CreatorAgentConfig = CreatorAgentConfig()


class SimulationModel(Model):
    def __init__(
        self,
        exchange: Exchange,
        config: SimulationModelConfig = SimulationModelConfig(),
    ):
        super().__init__()

        self.max_steps = config.max_steps

        self.progress = Bar("Processing", max=self.max_steps)

        self.schedule = RandomActivation(self)

        creator_agent = CreatorAgent(uuid.uuid4(), self, config.creator)

        self.schedule.add(creator_agent)

        self.exchange = exchange

        self.exchange.set_creator(creator_agent)

        self.agent_config_growth: List[
            Tuple[int, Callable[[float], float], TraderAgentConfig]
        ] = []

        for c in config.agents:
            agent_growth = curve_type_function[c.curve_config.curve_type](
                c.curve_config.curve_params
            )
            n_initial_agents = int(agent_growth(0))

            for _ in range(n_initial_agents):
                a = TraderAgent(uuid.uuid4(), self, c.agent_config)
                self.schedule.add(a)

            self.agent_config_growth.append(
                (
                    n_initial_agents,
                    agent_growth,
                    c.agent_config,
                )
            )

        self.datacollector = DataCollector(
            model_reporters={
                "Price": self.exchange.current_price,
                "Supply": lambda _: self.exchange.supply,
                "Reserve": lambda _: self.exchange.reserve,
            },
            agent_reporters={"Supply": "supply", "Reserve": "reserve"},
        )

    def __agent_arrival__(self):
        size = len(self.agent_config_growth)
        for _ in range(size):
            initial, growth, config = self.agent_config_growth.pop()

            i = initial
            for i in range(
                initial,
                floor(growth(self.schedule.steps)),
            ):
                a = TraderAgent(uuid.uuid4(), self, config)
                self.schedule.add(a)

            self.agent_config_growth.insert(0, (i, growth, config))

        print(" | Agents: %d\r" % len(self.schedule.agents), end="")

    def step(self):
        self.__agent_arrival__()

        self.datacollector.collect(self)

        if self.schedule.steps > self.max_steps:
            self.running = False
            self.progress.finish()
        else:
            self.schedule.step()
            self.progress.next()
