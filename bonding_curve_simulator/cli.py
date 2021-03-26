"""Console script for bonding_curve_simulator."""
from bonding_curve_simulator.bonding_curve_simulator import run_simulation
import sys
import click


@click.command()
def main(args=None):
    """Console script for bonding_curve_simulator."""

    # run_simulation()

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
