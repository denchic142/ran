from typing import Dict

import numpy as np
from sweep_design import Relation, ArrayAxis
from sweep_design.axis import get_array_axis_from_array

from receiver import SeismicPoint, Components
from point import Point


def get_seismic_points(
    file_name: str, delimiter: str, encoding=None, skip_header=0
) -> Dict[str, SeismicPoint]:
    seismic_points = {}

    with open(file_name, encoding=encoding) as f:
        cnt = 0
        for line in f.readlines():
            cnt += 1
            if cnt <= skip_header:
                continue

            data = line.split(sep=delimiter)
            if len(data) != 10:
                print(f"Point with name '{data[1]}' is incorrect! Row: {cnt}")
                continue

            coordinate = Point(
                x=data[3],
                y=data[4],
                z=data[5],
            )
            seismic_point = SeismicPoint(
                PointId=data[0],
                PointName=data[1],
                SysId=data[2],
                coordinate=coordinate,
                VPmean=data[6],
                VPdef=data[7],
                VSmean=data[8],
                VSdef=data[9],
            )

            seismic_points.update({seismic_point.PointName: seismic_point})

    return seismic_points


def get_data_seismic_points(
    filename: str,
    seismic_points: Dict[str, SeismicPoint],
    delimiter: str,
    time_axis: ArrayAxis = None,
    skip_header=0,
):
    names = np.genfromtxt(
        filename, dtype=np.str_, delimiter=delimiter, max_rows=skip_header
    )

    print(names)

    data = np.genfromtxt(
        filename,
        delimiter=delimiter,
        skip_header=skip_header,
    )

    if time_axis is None:
        time_axis = get_array_axis_from_array(data[:, 0])

    cnt = 0
    while True:
        if cnt * 3 + 1 > names.shape[0] - 1:
            break

        point_name = names[3 * cnt + 1].split("_")[0]

        seismic_point = seismic_points.get(point_name, None)

        if seismic_point is None:
            print(f"Point with name {point_name} is not found!")
            cnt += 1
            continue

        data_components = Components(
            x=Relation(time_axis, data[:, 3 * cnt + 1]),
            y=Relation(time_axis, data[:, 3 * cnt + 2]),
            z=Relation(time_axis, data[:, 3 * cnt + 3]),
        )

        seismic_point.data_components = data_components

        cnt += 1
