from typing import List

import unittest

from src.utils import IO
from src.animation.animation import Animation
from src.selection.error_matrix import ErrorMatrix
from src.selection.error_matrix_operation import ErrorMatrixOperation
from src.selection.error_matrix_library import ErrorMatrixLibrary


class TestErrorMatrix(unittest.TestCase):

    def test_setup(self):
        csv_filepath = "AnimationData/evaluation/run.csv"
        csv_from_csv_file_read = IO.read_csv_content_as_list_of_lists(csv_filepath)

        anim = Animation.character_animation_from_csv("AnimationData/animation/run.csv")
        op = ErrorMatrixOperation(ErrorMatrixLibrary.max_point_to_line_distance)
        error_matrix = ErrorMatrix.from_animation(anim, op)
        csv_from_error_matrix_object = error_matrix.as_csv()

        # Check shape is equal (same number of rows and columns)
        self.assertEqual(len(csv_from_error_matrix_object), len(csv_from_csv_file_read))
        for i in range(len(csv_from_error_matrix_object)):
            row_from_anim = csv_from_error_matrix_object[i]
            row_from_file = csv_from_csv_file_read[i]
            self.assertEqual(len(row_from_anim), len(row_from_file))

        # Check headers are equal
        row_from_anim = csv_from_error_matrix_object[0]
        row_from_file = csv_from_csv_file_read[0]
        self.assertEqual(row_from_anim, row_from_file)

        # Check parsed values are equal
        for i in range(1, len(csv_from_error_matrix_object)):
            row_from_anim = csv_from_error_matrix_object[i]
            row_from_file = csv_from_csv_file_read[i]
            for j in range(len(csv_from_error_matrix_object[i])):
                value_from_anim = float(row_from_anim[j])
                value_from_file = float(row_from_file[j])
                self.assertEqual(value_from_anim, value_from_file)
