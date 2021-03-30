from dataclasses import dataclass
from enum import Enum
from typing import Callable
import numpy as np


class CurveType(Enum):
    EXPONENTIAL = "exponential"
    LOGISTIC = "logistic"


# https://en.wikipedia.org/wiki/Generalised_logistic_function
@dataclass
class LogisticConfig:
    a: float = 0.0
    k: float = 1.0
    b: float = 3.0
    v: float = 0.5
    q: float = 0.5
    c: float = 1.0
    m: float = 3.0


@dataclass
class ExponentialConfig:
    m: float = 1.0 / 400
    n: float = 2.0
    y0: float = 0.0
    x0: float = 0.0


def exponential(config: ExponentialConfig) -> Callable[[float], float]:
    return lambda x: config.y0 + config.m * ((x - config.x0) ** config.n)


def logistic(config: LogisticConfig) -> Callable[[float], float]:
    return lambda x: config.a + (
        (config.k - config.a)
        / (config.c + ((config.q * np.e) ** (-config.b * (x - config.m))))
        ** (1 / config.v)
    )
