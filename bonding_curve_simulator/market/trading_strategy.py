from abc import ABC, abstractmethod
from bonding_curve_simulator.mesa.agent.trader import TraderAgent
from dataclasses import dataclass


@dataclass
class TradingStrategyConfig:
    sigma_n = 1000  # observation noise variance
    r_bar = 100000  # true mean fundamental value
    kappa = 0.05  # mean reversion parameter
    sigma_s = 100000  # shock variance
    q_max = 10  # max unit holdings
    sigma_pv = 5000000  # private value variance
    R_min = 0  # min requested surplus
    R_max = 250  # max requested surplus
    eta = 1.0  # strategic threshold
    lambda_a = 0.005  # mean arrival rate of ZI agents


class TradingStrategy(ABC):
    @abstractmethod
    def execute(self, agent: TraderAgent) -> None:
        raise NotImplementedError
