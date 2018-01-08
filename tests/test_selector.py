from src.selection.greedy import Greedy
from src.selection.salient import Salient
from tests.csv_test import CsvTest


class TestSelectors(CsvTest):
    def test_salient(self):
        self.load_animation("quadbot")
        self.load_error_matrix()
        selector = Salient("Salient", self.animation, self.error_matrix)
        selector.execute(12)
        self.compare_csv_output_to_file(selector.as_csv(False), "selection", "quadbot-Salient")

    def test_greedy(self):
        self.load_animation("quadbot")
        self.load_error_matrix()
        selector = Greedy("Greedy", self.animation, self.error_matrix)
        selector.execute(12)
        self.compare_csv_output_to_file(selector.as_csv(False), "selection", "quadbot-Greedy")
