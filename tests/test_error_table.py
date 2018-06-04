from SalientPosesReference.src.analysis.error_table import ErrorTable
from SalientPosesReference.src.analysis.error_table_library import ErrorTableLibrary
from SalientPosesReference.src.analysis.error_table_operation import ErrorTableOperation
from tests.csv_test import CsvTest


class TestErrorTable(CsvTest):

    """
    Builds an error table for the animation corresponding to `anim`.

    Note: the error table provides a `save()` method that can be used to generate the outputs used in these
          tests. 
    """
    def build_error_table_for_test_named(self, anim):
        self.load_animation(anim)
        op = ErrorTableOperation(ErrorTableLibrary.max_point_to_line_distance)
        error_table = ErrorTable.from_animation(self.animation, op)
        csv_output = error_table.as_csv()
        self.compare_csv_output_to_file(csv_output, "analysis", anim)

    def test_error_table(self):
        self.build_error_table_for_test_named("small")
