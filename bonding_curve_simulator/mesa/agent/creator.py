from __future__ import annotations
from bonding_curve_simulator.mesa.simulation_model import SimulationModel
from bonding_curve_simulator.market.growth_curves import (
    CurveConfig,
    curve_type_function,
)

from typing import TYPE_CHECKING, cast

from mesa import Agent
from pydantic.main import BaseModel


if TYPE_CHECKING:
    from bonding_curve_simulator.market.exchange import WealthConfig


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
        model = cast(SimulationModel, self.model)

        steps = model.schedule.steps

        model.exchange.reserve += self.growth_curve(steps)
