import csv
from _io import TextIOWrapper
from typing import List


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
        row_size = len(data[0])
        row_str = "%s," * (row_size - 1) + "%s\n"
        for row in data:
            data_str += row_str % tuple(row)

        f.write(data_str)
        f.close()


class TransformStringsInList:
    @staticmethod
    def as_floats(data: List[str]) -> List[float]:
        return [float(value) for value in data]


class TransformFloatsInList:
    @staticmethod
    def asStrings(data: List[float]) -> List[str]:
        return [str(value) for value in data]
