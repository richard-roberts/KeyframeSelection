import csv
from _io import TextIOWrapper
from typing import List

import numpy as np


class IO:
    @staticmethod
    def open_file_to_read(filepath: str) -> TextIOWrapper:
        return open(filepath, "r")

    @staticmethod
    def open_file_to_write(filepath: str) -> TextIOWrapper:
        return open(filepath, "w")

    @staticmethod
    def close(file: TextIOWrapper) -> None:
        file.close()

    @staticmethod
    def read_file_content_as_string(filepath: str) -> str:
        f = IO.open_file_to_read(filepath)
        ret = f.read()
        f.close()
        return ret

    @staticmethod
    def read_csv_content_as_list_of_lists(filepath: str) -> List[List[str]]:
        outer_list = []

        f = IO.open_file_to_read(filepath)
        for row in csv.reader(f, delimiter=','):
            inner_list = list(row)
            outer_list.append(inner_list)
        f.close()

        return outer_list

    @staticmethod
    def write_list_of_lists_as_csv(filepath: str, data: List[List[str]]) -> None:
        f = IO.open_file_to_write(filepath)

        data_str = ""
        for row in data:
            row_size = len(row)
            row_str = "%s," * (row_size - 1) + "%s\n"
            data_str += row_str % tuple(row)

        f.write(data_str)
        f.close()


class TransformStringsInList:
    @staticmethod
    def as_floats(data: List[str]) -> List[float]:
        return [float(value) for value in data]


class TransformFloatsInList:
    @staticmethod
    def as_strings(data: List[float]) -> List[str]:
        return [str(value) for value in data]


class Math:
    @staticmethod
    def finite_differences(points):
        tangents = []
        n = len(points)

        def get(i):
            if i == 0:
                return points[1] - points[0]
            elif i == n - 1:
                return points[-2] - points[-1]
            else:
                return points[i] - points[i+1]

        for i in range(n):
            t = get(i)
            t = t / np.linalg.norm(t)
            tangents.append(t)

        return tangents

    @staticmethod
    def linear_interpolation(a, b, t):
        return a + (b - a) * t

    @staticmethod
    def percentage_between(a, b, p):
        return (p - a) / (b - a)

    @staticmethod
    def sample_y_at_x_in_polyline(points, x: float):
        if int(x) == points[-1][0]:
            return points[-1][1]

        x_diff = x - points[0][0]
        ax, bx = int(np.floor(x_diff)), int(np.floor(x_diff)) + 1
        ay, by = points[ax][1], points[bx][1]
        return Math.linear_interpolation(ay, by, Math.percentage_between(ax, bx, x))

    @staticmethod
    def sample_y_at_x_in_polyline_d(points, x: float):
        if int(x) == points[-1][0]:
            return 0

        x_diff = x - points[0][0]
        ax, bx = int(np.floor(x_diff)), int(np.floor(x_diff)) + 1
        ay, by = points[ax][1], points[bx][1]
        return (by - ay) / (bx - ax)
