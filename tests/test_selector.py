from src.selection.greedy import Greedy
from src.selection.salient import Salient
from tests.csv_test import CsvTest


class TestSelectors(CsvTest):

    """
    Runs the selector corresponding to `selector_class` on the animation corresponding to `anim`.
     
    Note: the selector provides a `save()` method that can be used to generate the outputs used in these
          tests. 
    """
    
    def run_selector_on_test_named(self, selector_class, selector_name, anim):
        self.load_animation(anim)
        self.load_error_table()
        selector = selector_class(selector_name, self.animation, self.error_table)
        selector.execute()
        self.compare_csv_output_to_file(selector.as_csv(False), "selection", "%s-%s" % (anim, selector_name))

    def test_selectors(self):
        self.run_selector_on_test_named(Greedy, "Greedy", "small")
        self.run_selector_on_test_named(Salient, "Salient", "small")
