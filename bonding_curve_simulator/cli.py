"""Console script for bonding_curve_simulator."""
import sys
import click
import funcy
import yaml
from typing import Callable


from bonding_curve_simulator.mesa.simulation_model import SimulationModel
from bonding_curve_simulator.helpers.outfile import with_outfile
from bonding_curve_simulator.helpers.profiling import with_profiling
from bonding_curve_simulator.bonding_curve_simulator import (
    SimulationConfig,
    init_model,
    run_simulation,
)


@click.command()
@click.option(
    "--profile",
    help="Get cProfile information.",
    is_flag=True,
)
@click.option(
    "--outfile",
    help="Save datacollector results.",
    is_flag=True,
)
@click.argument("config-file", type=click.File("rb"), nargs=1)
def main(
    profile,
    outfile,
    config_file,
):

    config = yaml.full_load(config_file)

    model = init_model(SimulationConfig(**config))

    entrypoint = run_simulation

    if profile:
        entrypoint: Callable[
            [SimulationModel], SimulationModel
        ] = lambda model: with_profiling(lambda: run_simulation(model))

    if outfile:
        entrypoint = funcy.compose(with_outfile, entrypoint)

    entrypoint(model)

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
