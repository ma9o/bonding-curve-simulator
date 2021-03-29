from bonding_curve_simulator.mesa.simulation_model import SimulationModel
import cProfile
from pstats import SortKey, Stats
from io import StringIO
from typing import Callable


def with_profiling(run_simulation: Callable) -> SimulationModel:
    pr = None

    pr = cProfile.Profile()
    pr.enable()

    model = run_simulation()

    pr.disable()
    sortby = SortKey.CUMULATIVE
    s = StringIO()
    ps = Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    print(s.getvalue())

    return model
