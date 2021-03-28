"""Main module."""

from collections import defaultdict
from bonding_curve_simulator.market.exchange import (
    Exchange,
    ExchangeConfig,
    TaxConfig,
)
from bonding_curve_simulator.market.bonding_curve import (
    BondingCurve,
    CurveType,
    LogisticConfig,
    PowerConfig,
)
from typing import Dict, List
from bonding_curve_simulator.mesa.simulation_model import SimulationModel


# -> List[float]
def run_simulation(config=defaultdict(lambda: {})):

    curve_type = config["curve_type"] or CurveType.POWER
    curve_config_type = (
        LogisticConfig if curve_type == CurveType.LOGISTIC else PowerConfig
    )

    curve_config = curve_config_type(**config["curve_config"])
    exchange_config = ExchangeConfig(**config["exchange_config"])
    tax_config = TaxConfig(**config["tax_config"])

    exchange = Exchange(BondingCurve(curve_config), exchange_config, tax_config)

    model = SimulationModel(exchange)

    model.run_model()

    model.datacollector.get_model_vars_dataframe().to_csv("datacollector/model.csv")
    model.datacollector.get_agent_vars_dataframe().to_csv("datacollector/agent.csv")
