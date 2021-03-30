"""Main module."""

from bonding_curve_simulator.market.exchange import (
    Exchange,
    WealthConfig,
    TaxConfig,
    TaxType,
)
from bonding_curve_simulator.market.bonding_curve import (
    BondingCurve,
    CurveType,
    LogisticConfig,
    ExponentialConfig,
)
from typing import Dict, List
from bonding_curve_simulator.mesa.simulation_model import SimulationModel


def init_model(
    curve_type,
    curve_config,
    initial_supply,
    initial_reserve,
    tax_type,
    tax_amount,
    max_steps,
    max_agents,
    max_revenue,
):

    curve_config_type = (
        LogisticConfig if curve_type == CurveType.LOGISTIC else ExponentialConfig
    )

    curve_config = curve_config_type(**curve_config)

    exchange_config = WealthConfig(initial_supply, initial_reserve)
    tax_config = TaxConfig(tax_amount, tax_type)

    exchange = Exchange(BondingCurve(curve_config), exchange_config, tax_config)

    model = SimulationModel(exchange, max_steps, max_agents, max_revenue)

    return model


def run_simulation(model: SimulationModel) -> SimulationModel:
    model.run_model()

    return model