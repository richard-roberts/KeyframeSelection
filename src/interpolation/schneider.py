from SalientPosesReference.src.interpolation.interpolator import Interpolator


class Schneider(Interpolator):
    def execute(self):
        optimization_iterations = 10
        resolution = 100

        start = 0
        for curve, segment in zip(self.curves, self.segments):
            points = segment
            end = start + len(points) - 1

            t0 = self._tangents[start]
            t1 = self._tangents[end]

            for i in range(optimization_iterations):
                us = curve.parameters_nearest_to_points(points, resolution)
                curve.fit_to_points(points, t0, t1, us)

            start = end
