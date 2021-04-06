# Zero intelligence

# https://github.com/abides-sim/abides/blob/master/agent/ZeroIntelligenceAgent.py

# https://www.ncbi.nlm.nih.gov/pmc/articles/PMC548562/#__sec4title

# It suggests that institutions strongly shape our behavior, so that some of the properties of markets may depend
# more on the structure of institutions than on the rationality of individuals.

from __future__ import annotations

from typing import TYPE_CHECKING, cast

from bonding_curve_simulator.market.strategy.config import StrategyParams
from bonding_curve_simulator.market.strategy.strategy import Strategy

if TYPE_CHECKING:
    from bonding_curve_simulator.mesa.agent.trader import TraderAgent
    from bonding_curve_simulator.mesa.simulation_model import SimulationModel


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
        # TODO: use config
        r = agent.model.random.uniform(0, 1)

        if TYPE_CHECKING:
            model = cast(SimulationModel, agent.model)
        else:
            model = agent.model

        if r < 0.25:
            sale_amount = model.random.uniform(0, agent.supply)
            model.exchange.sell(agent, sale_amount)
        elif r > 0.5:
            reserve_amount = model.random.uniform(0.0, agent.reserve)
            model.exchange.buy(agent, reserve_amount)
        else:
            pass
