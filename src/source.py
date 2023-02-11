from dataclasses import dataclass
from datetime import datetime

from point import Point


@dataclass
class Source:
    name: str
    coordinate: Point