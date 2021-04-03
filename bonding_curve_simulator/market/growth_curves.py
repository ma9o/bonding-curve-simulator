from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable, Union
import numpy as np
from pydantic.main import BaseModel


class CurveType(Enum):
    EXPONENTIAL = "exponential"
    LOGISTIC = "logistic"


class CurveParams(BaseModel):
    y0 = 0.0
    x0 = 0.0


# https://en.wikipedia.org/wiki/Generalised_logistic_function
class LogisticParams(CurveParams):
    # q = x0
    # a = y0
    k = 1.0
    b = 3.0
    v = 0.5
    c = 1.0
    m = 3.0


class ExponentialParams(CurveParams):
    m = 1.0 / 400
    n = 2.0


class CurveConfig(BaseModel):
    curve_type: CurveType = CurveType.EXPONENTIAL
    curve_params: Union[LogisticParams, ExponentialParams] = ExponentialParams()


def exponential(params: ExponentialParams) -> Callable[[float], float]:
    return lambda x: params.y0 + params.m * ((x - params.x0) ** params.n)


def logistic(params: LogisticParams) -> Callable[[float], float]:
    return lambda x: params.y0 + (
        (params.k - params.y0)
        / (params.c + ((params.x0 * np.e) ** (-params.b * (x - params.m))))
        ** (1 / params.v)
    )


curve_type_function: dict[CurveType, Callable[[Any], Callable[[float], float]]] = {
    CurveType.EXPONENTIAL: exponential,
    CurveType.LOGISTIC: logistic,
}
