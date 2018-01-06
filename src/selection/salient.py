from typing import Dict, Tuple

from src.types import Time
from src.animation.timeline import Timeline
from src.animation.animation import Animation
from src.selection.error_matrix import ErrorMatrix
from src.selection.selection import Selection
from src.selection.selector import Selector


class Optimal:

    def __init__(self):
        self.selections: Dict[int, Tuple[Selection, float]] = {}

    def get(self, time: Time) -> Tuple[Selection, float]:
        return self.selections[time]

    def add(self, selection: Selection, error: float) -> None:
        self.selections[selection.last()] = (selection, error)


class Salient(Selector):

    def __init__(self, name: str, animation: Animation, error_matrix: ErrorMatrix):
        super().__init__(name, animation, error_matrix)

        self.last_optimal = Optimal()
        for end in self.animation.timeline.as_range()[1:]:
            timeline = Timeline.from_start_end(self.animation.timeline.start, end)
            selection_to_end = Selection.first_selection(timeline)
            error = self.error_matrix.value_of_max_error(timeline)
            self.last_optimal.add(selection_to_end, error)

    def compute(self):

        def find_best_selection(n_keyframes: int, start: Time, end: Time, curr_optimal: Optimal):
            min_error: float = float('inf')
            best_selection: Time = None

            first = int(start + n_keyframes - 2)
            last = int(end - 1)
            for k in range(first, last + 1):
                time = Time(k)
                selection_start_to_k, error_start_to_k = curr_optimal.get(time)
                error_k_to_end = self.error_matrix.value_of_max_error(Timeline.from_start_end(time, end))
                error_combined = max(error_start_to_k, error_k_to_end)
                if min_error > error_combined:
                    min_error = error_combined
                    best_selection = Selection.as_copy(Timeline.from_start_end(start, end), selection_start_to_k)
                    best_selection.add(end)

            return best_selection, min_error

        def compute_next_optimal(previous, curr_optimal: Optimal) -> Optimal:
            selection: Selection = Selection.as_copy(previous.timeline, previous)

            n_keyframes = previous.n_keyframes() + 1
            start = selection.first()
            end = selection.last()

            next_optimal: Optimal = Optimal()
            first = start + n_keyframes - 1
            last = end
            for curr_end in range(first, last + 1):
                selection_to_end, error = find_best_selection(n_keyframes, start, curr_end, curr_optimal)
                next_optimal.add(selection_to_end, error)

            return next_optimal

        optimal = compute_next_optimal(self.previous, self.last_optimal)
        curr_selection, _ = optimal.get(self.previous.last())
        self.selections.append(curr_selection)

        self.last_optimal = optimal
        self.previous = curr_selection
