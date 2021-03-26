"""Main module."""


from bonding_curve_simulator.market.exchange import Exchange
from bonding_curve_simulator.market.bonding_curve import BondingCurve
from typing import Dict, List
from bonding_curve_simulator.mesa.simulation_model import SimulationModel


def run_simulation(config: Dict = None) -> List[float]:

    exchange = Exchange(
        BondingCurve(config["curve_type"], config["curve_config"]),
        config["exchange_config"],
    )

    model = SimulationModel(exchange)

    model.run_model()

    return model.result