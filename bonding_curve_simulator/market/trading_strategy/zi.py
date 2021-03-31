# Zero intelligence

# https://github.com/abides-sim/abides/blob/master/agent/ZeroIntelligenceAgent.py

from bonding_curve_simulator.market.trading_strategy import TradingStrategy, TradingStrategyConfig
from bonding_curve_simulator.mesa.agent.trader import TraderAgent



class ZIStrategy(TradingStrategy):
    def __init__(self, config: TradingStrategyConfig):
        self.config = config

        # The agent maintains two priors: r_t and sigma_t (value and error estimates).
        self.r_t = self.config.r_bar
        self.sigma_t = 0

        # The agent must track its previous wake time, so it knows how many time
        # units have passed.
        self.prev_wake_time = None

        # The agent has a private value for each incremental unit.
        self.theta = [int(x) for x in sorted(
                np.roundrandom_state.normal(loc=0, scale=sqrt(sigma_pv), size=(q_max * 2))).tolist(),
                reverse=True)]


    def execute(self, agent: TraderAgent):
        return super().execute(agent)
