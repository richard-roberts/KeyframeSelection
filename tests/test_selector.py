import os

import unittest

from src.utils import IO
from src.animation.animation import Animation
from src.selection.error_matrix import ErrorMatrix
from src.selection.error_matrix_operation import ErrorMatrixOperation
from src.selection.error_matrix_library import ErrorMatrixLibrary
from src.selection.greedy import Greedy
from src.selection.salient import Salient


class TestSelectors(unittest.TestCase):

    def get_error_matrix(self, filepath, anim):
        op = ErrorMatrixOperation(ErrorMatrixLibrary.max_point_to_line_distance)

        if os.path.isfile(filepath):
            return ErrorMatrix.from_csv(filepath, anim, op)
        else:
            error_matrix = ErrorMatrix.from_animation(anim, op)
            error_matrix.save("tests/data")
            return error_matrix

    def compare_csv_output_to_file(self, csv_output, csv_filepath):
        csv_from_file = IO.read_csv_content_as_list_of_lists(csv_filepath)

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

    def test_salient(self):
        animation_filepath = "AnimationData/animation/quadbot.csv"
        evaluation_filepath = "AnimationData/evaluation/quadbot.csv"
        expected_filepath = "AnimationData/selection/quadbot-Salient.csv"

        anim: Animation = Animation.character_animation_from_csv(animation_filepath)
        error_matrix = self.get_error_matrix(evaluation_filepath, anim)
        selector = Salient("Salient", anim, error_matrix)
        selector.execute(12)

        csv_output = selector.as_csv(False)
        self.compare_csv_output_to_file(csv_output, expected_filepath)

    def test_greedy(self):
        animation_filepath = "AnimationData/animation/quadbot.csv"
        evaluation_filepath = "AnimationData/evaluation/quadbot.csv"
        expected_filepath = "AnimationData/selection/quadbot-Greedy.csv"

        anim: Animation = Animation.character_animation_from_csv(animation_filepath)
        error_matrix = self.get_error_matrix(evaluation_filepath, anim)
        selector = Greedy("Greedy", anim, error_matrix)
        selector.execute(12)

        csv_output = selector.as_csv(False)
        self.compare_csv_output_to_file(csv_output, expected_filepath)
