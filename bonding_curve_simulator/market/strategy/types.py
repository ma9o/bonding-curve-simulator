from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING, Type

from bonding_curve_simulator.globals import BaseModel
from bonding_curve_simulator.market.strategy.config import StrategyParams
from bonding_curve_simulator.market.strategy.strategies.hbf import HBFStrategy
from bonding_curve_simulator.market.strategy.strategies.momentum import MomentumStrategy
from bonding_curve_simulator.market.strategy.strategies.qlearn import QLearningStrategy
from bonding_curve_simulator.market.strategy.strategies.value import ValueStrategy
from bonding_curve_simulator.market.strategy.strategies.zi import ZIStrategy

if TYPE_CHECKING:
    from bonding_curve_simulator.market.strategy.strategy import Strategy


class StrategyType(Enum):
    ZI = "zi"
    HBF = "hbf"
    QLEARN = "qlearn"
    VALUE = "value"
    MOMENTUM = "momentum"


class StrategyConfig(BaseModel):
    strategy_type: StrategyType = StrategyType.ZI
    params: StrategyParams = StrategyParams()


strategy_type_class: dict[StrategyType, Type[Strategy]] = {
    StrategyType.ZI: ZIStrategy,
    StrategyType.HBF: HBFStrategy,
    StrategyType.QLEARN: QLearningStrategy,
    StrategyType.VALUE: ValueStrategy,
    StrategyType.MOMENTUM: MomentumStrategy,
}
