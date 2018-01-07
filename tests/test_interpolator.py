from typing import List

import unittest

from src.animation.animation import Animation
from src.selection.selection import Selection
from src.selection.selector import Selector
from src.interpolation.schneider import Schneider


class TestInterpolator(unittest.TestCase):

    def test_schneider(self):
        filepath: str = "AnimationData/animation/quadbot.csv"
        animation: Animation = Animation.character_animation_from_csv(filepath)
        selector: Selector = Selector.from_file("AnimationData/selection/quadbot-Salient.csv", animation)

        selection: Selection = selector.selections[6]
        dimensions: List[str] = animation.dimensions()

        dimension: str = dimensions[1]
        interpolator = Schneider(animation, selection, dimension)

        interpolator.execute()

        print("\n\n")
        for curve in interpolator.get_curves():
            print(curve)
