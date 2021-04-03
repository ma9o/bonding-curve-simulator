"""Console script for bonding_curve_simulator."""
import sys
from typing import Callable

import click
import funcy
import yaml
from devtools import debug

from bonding_curve_simulator.bonding_curve_simulator import (
    SimulationConfig,
    init_model,
    run_simulation,
)
from bonding_curve_simulator.helpers.output import with_outdir
from bonding_curve_simulator.helpers.profiling import with_profiling
from bonding_curve_simulator.mesa.simulation_model import SimulationModel


@click.command()
@click.option(
    "--profile",
    help="Get cProfile information.",
    is_flag=True,
)
@click.option(
    "--outdir", help="Save datacollector results.", type=click.Path(exists=True)
)
@click.argument("config-file", type=click.File("rb"), nargs=1)
def main(
    profile,
    outdir,
    config_file,
):

    config_dict = yaml.full_load(config_file)

    config = SimulationConfig.parse_obj(config_dict)

    debug(config)

    model = init_model(config)

    entrypoint = run_simulation

    if profile:
        entrypoint: Callable[
            [SimulationModel], SimulationModel
        ] = lambda model: with_profiling(lambda: run_simulation(model))

    if outdir:
        entrypoint = funcy.py3.compose(with_outdir(outdir), entrypoint)

    entrypoint(model)

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
