# https://github.com/abides-sim/abides/blob/master/agent/ValueAgent.py

from __future__ import annotations

from typing import TYPE_CHECKING

from bonding_curve_simulator.market.strategy.config import StrategyParams
from bonding_curve_simulator.market.strategy.strategy import Strategy

if TYPE_CHECKING:
    from bonding_curve_simulator.mesa.agent.trader import TraderAgent


class ValueStrategy(Strategy):
    def __init__(self, params: StrategyParams = StrategyParams()):
        self.params = params

    def execute(self, agent: TraderAgent):
        return super().execute(agent)
