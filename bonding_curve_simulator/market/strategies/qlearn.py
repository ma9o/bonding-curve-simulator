# https://github.com/abides-sim/abides/blob/master/agent/examples/QLearningAgent.py

from bonding_curve_simulator.mesa.agent.trader import TraderAgent
from bonding_curve_simulator.market.trading_strategy import Strategy


class QLearningStrategy(Strategy):
    def __init__(self, qtable) -> None:
        self.qtable = qtable

    def execute(self, agent: TraderAgent):
        return super().execute(agent)