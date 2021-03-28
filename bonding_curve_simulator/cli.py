"""Console script for bonding_curve_simulator."""
from bonding_curve_simulator.helpers.profiling import with_profiling
from bonding_curve_simulator.bonding_curve_simulator import run_simulation
import sys
import click


@click.command()
@click.option(
    "--profile",
    help="Get cProfile information.",
    is_flag=True,
)
def main(profile):
    if profile:
        with_profiling(run_simulation)
    else:
        run_simulation()

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
