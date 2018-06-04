from SalientPosesReference.src.interpolation.schneider import Schneider
from SalientPosesReference.src.interpolation.obcf import OptimizationBasedCurveFitting
from tests.csv_test import CsvTest


class TestInterpolators(CsvTest):

    """
    Runs the interpolator corresponding to `interpolator_class` on the given `dimension` of the given animation,
    in which the selection of `n` keyframes from the given selector are used. 
     
    Note: the interpolator provides a `save()` method that can be used to generate the outputs used in these
          tests
          
    Note: refer to the headers in the animation csv files (https://github.com/richard-roberts/AnimationData) for a list
          of the available dimensions
    """
    def run_interpolator_on_test_named(self, interpolator_class, interpolator_name, selector_name, n, anim, dimension):
        self.load_animation(anim)
        self.load_selector("%s-%s" % (anim, selector_name))
        selection = self.selector.selections[n - 2]
        interpolator = interpolator_class(interpolator_name, self.animation, selection, dimension)
        interpolator.execute()
        self.compare_csv_output_to_file(interpolator.as_csv(), "interpolation", "%s-%s" % (anim, interpolator_name))

    def test_interpolators(self):
        self.run_interpolator_on_test_named(Schneider, "Schneider", "Salient", 3, "small", "Bone-z")
        self.run_interpolator_on_test_named(OptimizationBasedCurveFitting, "OBCF", "Salient", 3, "small", "Bone-z")
