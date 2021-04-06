from enum import Enum
from typing import Any, Callable, Union

import numpy as np

from bonding_curve_simulator.globals import BaseModel


class CurveType(Enum):
    EXPONENTIAL = "exponential"
    LOGISTIC = "logistic"


# https://en.wikipedia.org/wiki/Generalised_logistic_function
class LogisticParams(BaseModel):
    q = 0.5
    a = 1
    k = 1.0
    b = 3.0
    v = 0.5
    c = 1.0
    m = 3.0


class ExponentialParams(BaseModel):
    y0 = 0.0
    x0 = 0.0
    m = 1.0 / 400
    n = 2.0


class CurveConfig(BaseModel):
    curve_type: CurveType = CurveType.EXPONENTIAL
    curve_params: Union[ExponentialParams, LogisticParams] = ExponentialParams()


def exponential(params: ExponentialParams) -> Callable[[float], float]:
    y0, m, x0, n = params.y0, params.m, params.x0, params.n

    return lambda x: y0 + (m * ((x - x0) ** n))


def logistic(params: LogisticParams) -> Callable[[float], float]:
    a, k, c, q, b, m, v = (
        params.a,
        params.k,
        params.c,
        params.q,
        params.b,
        params.m,
        params.v,
    )

    return lambda x: a + ((k - a) / (c + ((q * np.e) ** (-b * (x - m)))) ** (1 / v))


curve_type_function: dict[CurveType, Callable[[Any], Callable[[float], float]]] = {
    CurveType.EXPONENTIAL: exponential,
    CurveType.LOGISTIC: logistic,
}
