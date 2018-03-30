import unittest

from src.analysis.error_matrix import ErrorMatrix
from src.analysis.error_matrix_library import ErrorMatrixLibrary
from src.analysis.error_matrix_operation import ErrorMatrixOperation
from src.animation.animation import Animation
from src.selection.selector import Selector
from src.utils import IO


class CsvTest(unittest.TestCase):
    directory = "AnimationData"

    def __init__(self, method_name):
        super().__init__(method_name)
        self.animation: Animation = None
        self.error_matrix: ErrorMatrix = None
        self.selector: Selector = None

    def load_animation(self, filename):
        filepath = "%s/animation/%s.csv" % (CsvTest.directory, filename)
        self.animation = Animation.character_animation_from_csv(filepath)

    def load_error_matrix(self):
        filepath = "%s/evaluation/%s.csv" % (CsvTest.directory, self.animation.name)
        op = ErrorMatrixOperation(ErrorMatrixLibrary.max_point_to_line_distance)
        self.error_matrix = ErrorMatrix.from_csv(filepath, self.animation, op)

    def load_selector(self, filename):
        filepath = "%s/selection/%s.csv" % (CsvTest.directory, filename)
        self.selector = Selector.from_file(filepath, self.animation)

    def compare_csv_output_to_file(self, csv_output, directory, filename):
        filepath = "%s/%s/%s.csv" % (CsvTest.directory, directory, filename)
        csv_from_file = IO.read_csv_content_as_list_of_lists(filepath)

        # Check shape is equal (same number of rows and columns)
        self.assertEqual(len(csv_output), len(csv_from_file))
        for i in range(len(csv_output)):
            row_from_anim = csv_output[i]
            row_from_file = csv_from_file[i]
            self.assertEqual(len(row_from_anim), len(row_from_file))

        # Check headers are equal
        row_from_anim = csv_output[0]
        row_from_file = csv_from_file[0]
        self.assertEqual(row_from_anim, row_from_file)

        # Check parsed values are equal
        for i in range(1, len(csv_output)):
            row_from_anim = csv_output[i]
            row_from_file = csv_from_file[i]
            for j in range(len(csv_output[i])):
                value_from_anim = float(row_from_anim[j])
                value_from_file = float(row_from_file[j])
                self.assertEqual(value_from_anim, value_from_file)
