from src.analysis.error_matrix import ErrorMatrix
from src.analysis.error_matrix_library import ErrorMatrixLibrary
from src.analysis.error_matrix_operation import ErrorMatrixOperation
from tests.csv_test import CsvTest


class TestErrorMatrix(CsvTest):
    def test_setup(self):
        self.load_animation("run")
        self.load_error_matrix()
        op = ErrorMatrixOperation(ErrorMatrixLibrary.max_point_to_line_distance)
        error_matrix = ErrorMatrix.from_animation(self.animation, op)
        csv_output = error_matrix.as_csv()
        self.compare_csv_output_to_file(csv_output, "evaluation", "run")
