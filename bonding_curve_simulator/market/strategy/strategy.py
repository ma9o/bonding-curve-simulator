from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bonding_curve_simulator.mesa.agent.trader import TraderAgent


class Strategy(ABC):
    @abstractmethod
    def __init__(self, params) -> None:
        raise NotImplementedError

    @abstractmethod
    def execute(self, agent: TraderAgent) -> None:
        raise NotImplementedError
