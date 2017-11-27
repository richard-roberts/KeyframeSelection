from typing import List

import unittest

from src.utils import IO
from src.setup.animation import CreateAnimation
from src.scene.things.character import Character
from src.scene.coordinates.joint import Joint


class TestAnimation(unittest.TestCase):

    def test_setup(self):
        filepath: str = "tests/data/walk-animation.csv"
        animation = CreateAnimation.from_csv(filepath, Character, Joint)
        csv_from_animation_object: List[List[str]] = animation.as_csv()
        csv_from_csv_file_read: List[List[str]] = IO.read_csv_content_as_list_of_lists(filepath)

        # Check shape is equal (same number of rows and columns)
        self.assertEqual(len(csv_from_animation_object), len(csv_from_csv_file_read))
        for i in range(len(csv_from_animation_object)):
            row_from_anim = csv_from_animation_object[i]
            row_from_file = csv_from_csv_file_read[i]
            self.assertEqual(len(row_from_anim), len(row_from_file))

        # Check headers are equal
        row_from_anim = csv_from_animation_object[0]
        row_from_file = csv_from_csv_file_read[0]
        self.assertEqual(row_from_anim, row_from_file)

        # Check parsed values are equal
        for i in range(1, len(csv_from_animation_object)):
            row_from_anim = csv_from_animation_object[i]
            row_from_file = csv_from_csv_file_read[i]
            for j in range(len(csv_from_animation_object[i])):
                value_from_anim = float(row_from_anim[j])
                value_from_file = float(row_from_file[j])
                self.assertEqual(value_from_anim, value_from_file)