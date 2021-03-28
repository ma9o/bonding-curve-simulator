import cProfile
from pstats import SortKey, Stats
from io import StringIO
from typing import Callable


def with_profiling(entrypoint: Callable):
    pr = None

    pr = cProfile.Profile()
    pr.enable()

    entrypoint()

    pr.disable()
    sortby = SortKey.CUMULATIVE
    s = StringIO()
    ps = Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    print(s.getvalue())
