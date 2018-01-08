from src.interpolation.schneider import Schneider
from src.selection.selection import Selection
from tests.csv_test import CsvTest


class TestInterpolators(CsvTest):
    def test_schneider(self):
        self.load_animation("quadbot")
        self.load_selector("quadbot-Salient")
        selection: Selection = self.selector.selections[6]
        dimension: str = self.animation.dimensions()[1]
        interpolator = Schneider("Schneider", self.animation, selection, dimension)
        interpolator.execute()
        self.compare_csv_output_to_file(interpolator.as_csv(), "interpolation", "quadbot-Schneider")
