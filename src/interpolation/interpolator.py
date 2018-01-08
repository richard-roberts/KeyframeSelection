import os
import copy
from typing import List

from src.animation.animation import Animation
from src.interpolation.curve import Curve
from src.selection.selection import Selection
from src.utils import IO, Math


class Interpolator(object):
    def __init__(self, name: str, animation: Animation, selection: Selection, dimension: str):
        self.name = name
        self.animation = animation
        self._curve = self.animation.get_curve_for_dimension(dimension)
        self._tangents = Math.finite_differences(self._curve)
        self._animation = animation
        self._selection = selection

        s, e = animation.timeline.start, animation.timeline.end
        self.segments = []
        for a, b in selection.get_pairs():
            index_from = a - s
            index_to = b - s
            segment = self._curve[index_from: index_to + 1]
            self.segments.append(segment)

        self.curves = []
        for (segment, (a, b)) in zip(self.segments, selection.get_pairs()):
            index_from = a - s
            index_to = b - s
            tangent_from = self._tangents[index_from]
            tangent_to = self._tangents[index_to]
            curve = Curve.create_by_fitting_points(segment, tangent_from, tangent_to)
            self.curves.append(curve)

    def get_curves(self):
        return copy.deepcopy(self.curves)

    def execute(self):
        raise NotImplementedError

    def as_csv(self) -> List[List[str]]:
        header = ["A.x", "A.y", "B.x", "B.y", "C.x", "C.y", "D.x", "D.y"]
        body = []
        for curve in self.curves:
            row = [
                "%2.4f" % round(curve.get_a()[0], 4), "%2.4f" % round(curve.get_a()[1], 4),
                "%2.4f" % round(curve.get_b()[0], 4), "%2.4f" % round(curve.get_b()[1], 4),
                "%2.4f" % round(curve.get_c()[0], 4), "%2.4f" % round(curve.get_c()[1], 4),
                "%2.4f" % round(curve.get_d()[0], 4), "%2.4f" % round(curve.get_d()[1], 4)
            ]
            body.append(row)

        return [header] + body

    def save(self, directory: str):
        IO.write_list_of_lists_as_csv("%s/%s-%s.csv" % (directory, self.animation.name, self.name), self.as_csv())

    @staticmethod
    def from_file(filepath: str, animation: Animation, selection: Selection, dimension: str):
        csv = IO.read_csv_content_as_list_of_lists(filepath)

        interpolator = Interpolator(os.path.basename(filepath), animation, selection, dimension)
        for index, row in enumerate(csv[1:]):
            curve: Curve = interpolator.curves[index]
            curve.set_b(row[2], row[3])
            curve.set_c(row[4], row[5])

        return interpolator
