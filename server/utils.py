"""
Utility structures and functions.

Adin Ackerman
"""

from dataclasses import dataclass
from typing import TypeVar, Generic

T = TypeVar('T')


@dataclass
class Triple(Generic[T]):
    x: T
    y: T
    z: T

    def __iter__(self):
        yield from (self.x, self.y, self.z)
