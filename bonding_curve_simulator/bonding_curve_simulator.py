"""Main module."""

from bonding_curve_simulator.market.exchange import (
    Exchange,
    ExchangeConfig,
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
    curve_type=CurveType.EXPONENTIAL,
    curve_config=ExponentialConfig(),
    initial_supply=100.0,
    initial_reserve=100.0,
    tax_type=TaxType.RELATIVE,
    tax_amount=0.0,
):

    curve_config_type = (
        LogisticConfig if curve_type == CurveType.LOGISTIC else ExponentialConfig
    )

    curve_config = curve_config_type(**curve_config)

    exchange_config = ExchangeConfig(initial_supply, initial_reserve)
    tax_config = TaxConfig(tax_amount, tax_type)

    exchange = Exchange(BondingCurve(curve_config), exchange_config, tax_config)

    model = SimulationModel(exchange)

    return model


def run_simulation(model: SimulationModel) -> SimulationModel:
    model.run_model()

    return model