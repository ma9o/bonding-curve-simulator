# https://github.com/abides-sim/abides/blob/master/agent/examples/MomentumAgent.py

from bonding_curve_simulator.mesa.agent.trader import TraderAgent
from dataclasses import dataclass
from bonding_curve_simulator.market.trading_strategy import Strategy


@dataclass
class MomentumStrategyconfig:
    min_size = 1
    max_size = 100


class MomentumStrategy(Strategy):
    def __init__(self, config: MomentumStrategyconfig) -> None:
        self.config = config

    def execute(self, agent: TraderAgent):
        return super().execute(agent)
