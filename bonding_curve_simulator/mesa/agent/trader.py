from __future__ import annotations

from typing import TYPE_CHECKING

from mesa import Agent

from bonding_curve_simulator.globals import BaseModel
from bonding_curve_simulator.market.exchange.types import WealthConfig
from bonding_curve_simulator.market.strategy.types import (
    StrategyConfig,
    strategy_type_class,
)

if TYPE_CHECKING:
    from bonding_curve_simulator.mesa.simulation_model import SimulationModel


class TraderAgentConfig(BaseModel):
    strategy_config: StrategyConfig = StrategyConfig()
    wealth_config: WealthConfig = WealthConfig()


class TraderAgent(Agent):
    def __init__(
        self,
        unique_id,
        model: SimulationModel,
        config: TraderAgentConfig,
    ):
        super().__init__(unique_id, model)
        self.supply = config.wealth_config.supply
        self.reserve = config.wealth_config.reserve
        self.trading_strategy = strategy_type_class[
            config.strategy_config.strategy_type
        ](config.strategy_config.params)

    def step(self):
        self.trading_strategy.execute(self)
