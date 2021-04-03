# https://github.com/abides-sim/abides/blob/master/agent/examples/QLearningAgent.py


from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bonding_curve_simulator.mesa.agent.trader import TraderAgent

from bonding_curve_simulator.market.strategy.strategy import Strategy


class QLearningStrategy(Strategy):
    def __init__(self, qtable) -> None:
        self.qtable = qtable

    def execute(self, agent: TraderAgent):
        return super().execute(agent)