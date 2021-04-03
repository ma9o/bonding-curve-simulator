# Zero intelligence

# https://github.com/abides-sim/abides/blob/master/agent/ZeroIntelligenceAgent.py
from __future__ import annotations

from bonding_curve_simulator.market.strategy.config import StrategyParams
from bonding_curve_simulator.market.strategy.strategy import Strategy
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bonding_curve_simulator.mesa.agent.trader import TraderAgent


class ZIStrategy(Strategy):
    def __init__(self, params: StrategyParams = StrategyParams()):
        self.params = params

        # The agent maintains two priors: r_t and sigma_t (value and error estimates).
        self.r_t = self.params.r_bar
        self.sigma_t = 0

        # The agent must track its previous wake time, so it knows how many time
        # units have passed.
        self.prev_wake_time = None

        # The agent has a private value for each incremental unit.
        # self.theta = [int(x) for x in sorted(
        #         np.roundrandom_state.normal(loc=0, scale=sqrt(sigma_pv), size=(q_max * 2))).tolist(),
        #         reverse=True)]

    def execute(self, agent: TraderAgent):
        return super().execute(agent)
