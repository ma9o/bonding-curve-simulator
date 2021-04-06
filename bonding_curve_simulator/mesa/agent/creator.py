from __future__ import annotations

from typing import TYPE_CHECKING, cast

from mesa import Agent

from bonding_curve_simulator.globals import BaseModel
from bonding_curve_simulator.market.exchange.types import WealthConfig
from bonding_curve_simulator.market.growth_curves import (
    CurveConfig,
    curve_type_function,
)

if TYPE_CHECKING:
    from bonding_curve_simulator.mesa.simulation_model import SimulationModel


class CreatorAgentConfig(BaseModel):
    wealth_config: WealthConfig = WealthConfig()
    curve_config: CurveConfig = CurveConfig()


class CreatorAgent(Agent):
    def __init__(
        self,
        unique_id,
        model,
        config: CreatorAgentConfig,
    ):
        super().__init__(unique_id, model)
        self.reserve = config.wealth_config.reserve
        self.supply = config.wealth_config.supply
        self.growth_curve = curve_type_function[config.curve_config.curve_type](
            config.curve_config.curve_params
        )

    def step(self):
        if TYPE_CHECKING:
            model = cast(SimulationModel, self.model)
        else:
            model = self.model

        steps = model.schedule.steps

        if steps % 30 == 0:
            self.reserve += self.growth_curve(steps)
            model.exchange.buy(self, self.reserve)
