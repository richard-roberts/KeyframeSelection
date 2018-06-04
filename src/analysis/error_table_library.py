import numpy as np
from SalientPosesReference.src.interpolation.curve import Curve

class ErrorTableLibrary:
    @staticmethod
    def max_point_to_line_distance(points):

        start = points[0]
        end = points[-1]
        es = end - start

        def distance_between_line_and_point(point):
            ps = point - start
            numerator = np.dot(ps, es)
            denominator = np.dot(es, es)

            if denominator == 0.0:
                return 999999999.0
            else:
                ratio = numerator / denominator
                return np.linalg.norm(ps - ratio * es)

        max_distance = 0.0
        index_of_max_distance = -1

        for i, p in enumerate(points):
            curr_distance = distance_between_line_and_point(p)
            if curr_distance > max_distance:
                max_distance = curr_distance
                index_of_max_distance = i

        return max_distance, index_of_max_distance

    @staticmethod
    def max_curve_distance_to_line(points):
        curve = Curve.create_by_fitting_points_free(points)

        def max_distance_between_curve_and_point(point):
            interp = curve.point_nearest_to_point(point, 100)
            return np.linalg.norm(point - interp)

        max_distance = 0.0
        index_of_max_distance = -1
        for i, p in enumerate(points):
            curr_distance = max_distance_between_curve_and_point(p)
            if curr_distance > max_distance:
                max_distance = curr_distance
                index_of_max_distance = i
        return max_distance, index_of_max_distance
