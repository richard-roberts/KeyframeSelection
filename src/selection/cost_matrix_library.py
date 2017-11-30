import numpy as np


class CostMatrixLibrary:

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
        for p in points:
            curr_distance = distance_between_line_and_point(p)
            if curr_distance > max_distance:
                max_distance = curr_distance
        return max_distance
