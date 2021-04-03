# https://github.com/abides-sim/abides/blob/master/agent/examples/MomentumAgent.py

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bonding_curve_simulator.mesa.agent.trader import TraderAgent


from bonding_curve_simulator.market.strategy.strategy import Strategy
from dataclasses import dataclass


@dataclass
class MomentumStrategyconfig:
    min_size = 1
    max_size = 100


class MomentumStrategy(Strategy):
    def __init__(self, config: MomentumStrategyconfig) -> None:
        self.config = config

    def execute(self, agent: TraderAgent):
        return super().execute(agent)
