"""Main module."""

from bonding_curve_simulator.market.exchange.exchange import Exchange
from bonding_curve_simulator.market.exchange.types import ExchangeConfig
from pydantic.main import BaseModel
from bonding_curve_simulator.mesa.simulation_model import (
    SimulationModel,
    SimulationModelConfig,
)


class SimulationConfig(BaseModel):
    model_config: SimulationModelConfig = SimulationModelConfig()
    exchange_config: ExchangeConfig = ExchangeConfig()


def init_model(simulation_config: SimulationConfig = SimulationConfig()):

    exchange = Exchange(simulation_config.exchange_config)

    model = SimulationModel(exchange, simulation_config.model_config)

    return model


def run_simulation(model: SimulationModel) -> SimulationModel:
    model.run_model()

    return model