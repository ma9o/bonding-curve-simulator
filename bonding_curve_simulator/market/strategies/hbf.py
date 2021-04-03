# Heuristic Belief Learning

# https://github.com/abides-sim/abides/blob/master/agent/HeuristicBeliefLearningAgent.py


from bonding_curve_simulator.mesa.agent.trader import TraderAgent
from bonding_curve_simulator.market.trading_strategy import (
    Strategy,
    StrategyConfig,
)


class HBFStrategy(Strategy):
    def __init__(self, config: StrategyConfig):
        self.config = config

    def execute(self, agent: TraderAgent):
        return super().execute(agent)