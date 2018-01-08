from colors import GrayMid, RedDark
from pyplot import Axes, Draw, Figure
from src.animation.animation import Animation
from src.interpolation.interpolator import Interpolator
from src.interpolation.obcf import OptimizationBasedCurveFitting
from src.interpolation.schneider import Schneider
from src.selection.selection import Selection
from src.selection.selector import Selector

res_x = 1920
res_y = 1280


def draw_interpolation_results(directory: str, filename: str, animation: Animation, dimension: str,
                               selection: Selection, interpolator: Interpolator):
    points = animation.get_curve_for_dimension(dimension)
    min_y = min(p[1] for p in points)
    max_y = max(p[1] for p in points)

    Figure.new(res_x, res_y)
    Axes.set_axes_color(GrayMid())
    Axes.set_x_range(animation.timeline.start, animation.timeline.end)
    Axes.set_y_range(min_y, max_y)
    Axes.move_axis_to_center()

    Draw.lines(points, color=GrayMid(), zorder=1)
    Draw.points([points[i] for i in selection.as_zero_indexed_integers()], size=20, color=RedDark(), zorder=2)

    for curve in interpolator.curves:
        points = curve.sample_uniform(10)
        Draw.lines([curve.get_a(), curve.get_b()])
        Draw.lines([curve.get_c(), curve.get_d()])
        Draw.lines(points, color=RedDark(), linestyle="--")

    Figure.save(directory, filename)


def exe():
    animation: Animation = Animation.character_animation_from_csv("AnimationData/animation/quadbot.csv")
    selector: Selector = Selector.from_file("AnimationData/selection/quadbot-Salient.csv", animation)
    selection: Selection = selector.selections[6]
    dimension: str = animation.dimensions()[1]

    interpolator = Schneider("Schneider", animation, selection, dimension)
    interpolator.execute()
    draw_interpolation_results("~/Desktop/tmp", "Schneider", animation, dimension, selection, interpolator)

    interpolator = OptimizationBasedCurveFitting("OBCF", animation, selection, dimension)
    interpolator.execute()
    draw_interpolation_results("~/Desktop/tmp", "OBCF", animation, dimension, selection, interpolator)


if __name__ == "__main__":
    exe()
