from abc import ABC, abstractmethod
from typing import Type
from bonding_curve_simulator.market.strategies.zi import ZIStrategy
from bonding_curve_simulator.market.strategies.hbf import HBFStrategy
from bonding_curve_simulator.market.strategies.qlearn import QLearningStrategy
from bonding_curve_simulator.market.strategies.momentum import MomentumStrategy
from bonding_curve_simulator.market.strategies.value import ValueStrategy

from enum import Enum
from pydantic.main import BaseModel
from bonding_curve_simulator.mesa.agent.trader import TraderAgent


class StrategyType(Enum):
    ZI = "zi"
    HBF = "hbf"
    QLEARN = "qlearn"
    VALUE = "value"
    MOMENTUM = "momentum"


class StrategyParams(BaseModel):
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


class StrategyConfig(BaseModel):
    strategy_type: StrategyType = StrategyType.ZI
    params: StrategyParams = StrategyParams()


class Strategy(ABC):
    @abstractmethod
    def __init__(self, params) -> None:
        raise NotImplementedError

    @abstractmethod
    def execute(self, agent: TraderAgent) -> None:
        raise NotImplementedError


strategy_type_class: dict[StrategyType, Type[Strategy]] = {
    StrategyType.ZI: ZIStrategy,
    StrategyType.HBF: HBFStrategy,
    StrategyType.QLEARN: QLearningStrategy,
    StrategyType.VALUE: ValueStrategy,
    StrategyType.MOMENTUM: MomentumStrategy,
}
