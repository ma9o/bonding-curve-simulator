"""Console script for bonding_curve_simulator."""
import sys
import click
from funcy import compose
from typing import Callable


from bonding_curve_simulator.mesa.simulation_model import SimulationModel
from bonding_curve_simulator.helpers.outfile import with_outfile
from bonding_curve_simulator.market.exchange import TaxType
from bonding_curve_simulator.market.bonding_curve import CurveType
from bonding_curve_simulator.helpers.profiling import with_profiling
from bonding_curve_simulator.bonding_curve_simulator import init_model, run_simulation


@click.command()
@click.option(
    "--curve-type",
    default=CurveType.EXPONENTIAL.value,
    show_default=True,
    type=click.Choice([e.value for e in CurveType]),
)
@click.option("--initial-supply", show_default=True, type=click.FLOAT, default=100.0)
@click.option("--initial-reserve", show_default=True, type=click.FLOAT, default=100.0)
@click.option(
    "--tax-type",
    show_default=True,
    type=click.Choice([e.value for e in TaxType]),
    default=TaxType.RELATIVE.value,
)
@click.option(
    "--tax-amount",
    show_default=True,
    type=click.FLOAT,
    default=0.0,
)
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
@click.argument("curve-config", nargs=-1)
def main(
    curve_type,
    initial_supply,
    initial_reserve,
    tax_type,
    tax_amount,
    profile,
    outfile,
    curve_config,
):

    model = init_model(
        CurveType(curve_type),
        dict(curve_config),
        initial_supply,
        initial_reserve,
        TaxType(tax_type),
        tax_amount,
    )

    entrypoint = run_simulation

    if profile:
        entrypoint: Callable[
            [SimulationModel], SimulationModel
        ] = lambda model: with_profiling(lambda: run_simulation(model))

    if outfile:
        entrypoint = compose(with_outfile, entrypoint)

    entrypoint(model)

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
