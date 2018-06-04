from SalientPosesReference.src.analysis.error_table import ErrorTable
from SalientPosesReference.src.animation.animation import Animation
from SalientPosesReference.src.animation.timeline import Timeline
from SalientPosesReference.src.selection.selection import Selection
from SalientPosesReference.src.selection.selector import Selector


class Greedy(Selector):
    def __init__(self, name: str, animation: Animation, error_table: ErrorTable):
        super().__init__(name, animation, error_table)

    def compute(self):

        selection: Selection = Selection.as_copy(self.animation.timeline, self.previous)

        max_error: float = 0
        time_of_max_error: int = -1

        for (start, end) in selection.get_pairs():
            timeline: Timeline = Timeline.from_start_end(start, end)
            error: float = self.error_table.value_of_max_error(timeline)
            if error > max_error:
                max_error = error
                index_of_max_error = self.error_table.index_of_max_error(timeline)
                time_of_max_error = timeline.index_to_time(index_of_max_error)

        selection.add_with_error_on_duplicate(time_of_max_error)

        self.selections.append(selection)
        self.previous = selection
