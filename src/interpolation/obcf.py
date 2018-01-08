from typing import List

import numpy as np
from scipy.optimize import minimize

from src.interpolation.curve import Curve
from src.interpolation.interpolator import Interpolator
from src.utils import Math


class Energy:
    @staticmethod
    def accuracy(original_curve, curves: List[Curve]):
        total_e = 0

        for curve in curves:
            n = 10
            interps = curve.sample_uniform(n)

            for interp in interps:
                org_y = Math.sample_y_at_x_in_polyline(original_curve, interp[0])
                e = np.power(org_y - interp[1], 2)
                total_e += e

        return total_e

    @staticmethod
    def accuracy_d(original_curve, curves: List[Curve]):
        jacobian = [0.0 for _ in range(4 * len(curves))]

        for i, curve in enumerate(curves):
            n = 10
            interps = curve.sample_uniform(n)

            us = Curve.uniform_sample_set(n)
            for u, interp in zip(us, interps):
                org_y = Math.sample_y_at_x_in_polyline(original_curve, interp[0])
                org_y_d = Math.sample_y_at_x_in_polyline_d(original_curve, interp[0])
                jacobian[i * 4 + 0] += 2 * (interp[1] - org_y) * (-org_y_d * Curve.coefficient_b(u))
                jacobian[i * 4 + 1] += 2 * (interp[1] - org_y) * Curve.coefficient_b(u)
                jacobian[i * 4 + 2] += 2 * (interp[1] - org_y) * (-org_y_d * Curve.coefficient_c(u))
                jacobian[i * 4 + 3] += 2 * (interp[1] - org_y) * Curve.coefficient_c(u)

        return jacobian

    @staticmethod
    def colinear(_, curves):
        total_e = 0

        n = len(curves) - 1
        for i in range(n):
            x1, y1 = curves[i].get_c()
            x2, y2 = curves[i + 1].get_b()
            dx, dy = curves[i].get_d()

            v1 = np.arctan2((dy - y1), (dx - x1))
            v2 = np.arctan2((dy - y2), (dx - x2))

            if v1 >= 0 and v2 >= 0:
                pass
            elif v2 <= 0 <= v1:
                v2 += 2 * np.pi
            elif v1 <= 0 <= v2:
                v1 += 2 * np.pi
            else:
                v1 += 2 * np.pi
                v2 += 2 * np.pi

            angle = v1 - v2
            abs_angle = np.sqrt(np.power(angle, 2))
            e = np.power(abs_angle - np.pi, 2)
            total_e += e

        return total_e

    @staticmethod
    def colinear_d(_, curves):
        j = []
        j.append(0)
        j.append(0)

        n = len(curves) - 1
        for i in range(n):
            x1, y1 = curves[i].get_c()
            x2, y2 = curves[i + 1].get_b()
            dx, dy = curves[i].get_d()

            v1 = np.arctan2((dy - y1), (dx - x1))
            v2 = np.arctan2((dy - y2), (dx - x2))
            sq_xy = np.power(dy - y1, 2) + np.power(dx - x1, 2)
            sq_zw = np.power(dy - y2, 2) + np.power(dx - x2, 2)

            if v1 >= 0 and v2 >= 0:
                angle = v1 - v2
            elif v1 >= 0 >= v2:
                angle = v1 - v2 - 2 * np.pi
            elif v1 <= 0 <= v2:
                angle = v1 - v2 + 2 * np.pi
            else:
                angle = v1 - v2

            abs_angle = np.sqrt(np.power(angle, 2))
            j.append((2 * (dy - y1) * angle * (abs_angle - np.pi)) / (abs_angle * sq_xy))
            j.append(-(2 * (dx - x1) * angle * (abs_angle - np.pi)) / (abs_angle * sq_xy))
            j.append(-(2 * (dy - y2) * angle * (abs_angle - np.pi)) / (abs_angle * sq_zw))
            j.append((2 * (dx - x2) * angle * (abs_angle - np.pi)) / (abs_angle * sq_zw))

        j.append(0)
        j.append(0)
        return j


class OptimizationBasedCurveFitting(Interpolator):
    weight_distance = 1.0
    weight_colinear = 1000.0

    def set_current_solution(self, solution):
        n = len(self.curves)
        for i in range(n):
            x1 = solution[i * 4 + 0]
            y1 = solution[i * 4 + 1]
            x2 = solution[i * 4 + 2]
            y2 = solution[i * 4 + 3]
            self.curves[i].set_b(x1, y1)
            self.curves[i].set_c(x2, y2)
            self.curves[i].update()

    def get_current_solution(self):
        solution = []
        n = len(self.curves)
        for i in range(n):
            x1, y1 = self.curves[i].get_b()
            x2, y2 = self.curves[i].get_c()
            solution += [x1, y1, x2, y2]
        return solution

    def evaluate(self):
        es = [Energy.accuracy(self._curve, self.curves) * OptimizationBasedCurveFitting.weight_distance,
              Energy.colinear(self._curve, self.curves) * OptimizationBasedCurveFitting.weight_colinear]
        total_e = sum(es)
        return total_e

    def jacobian(self):
        js = [0 for _ in range(4 * len(self.curves))]

        for i, v in enumerate(Energy.accuracy_d(self._curve, self.curves)):
            js[i] += v * OptimizationBasedCurveFitting.weight_distance

        for i, v in enumerate(Energy.colinear_d(self._curve, self.curves)):
            js[i] += v * OptimizationBasedCurveFitting.weight_colinear

        return np.array(js)

    def set_and_evaluate(self, solution):
        self.set_current_solution(solution)
        return self.evaluate(), self.jacobian()

    def execute(self):
        result = minimize(self.set_and_evaluate, self.get_current_solution(), method="BFGS", jac=True)
        self.set_current_solution(result.x)
