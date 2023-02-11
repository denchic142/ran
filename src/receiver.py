from dataclasses import dataclass

from sweep_design import Relation

from point import Point


@dataclass
class Components:
    x: Relation = None
    y: Relation = None
    z: Relation = None


@dataclass
class SeismicPoint:
    PointId: int
    PointName: str
    SysId: int
    coordinate: Point = None
    data_components: Components = None
    VPmean: float = None
    VPdef: str = None
    VSmean: float = None
    VSdef: str = None
