from typing import List, Tuple
from multiprocessing.dummy import Pool as ThreadPool


from src.animation.timeline import Timeline
from src.types import Time
from src.animation.animation import Animation
from src.selection.selection import Selection
from src.selection.error_matrix_operation import ErrorMatrixOperation
from src.utils import IO, TransformStringsInList


class ErrorMatrix:
    def __init__(self, animation: Animation, operation: ErrorMatrixOperation):
        self.animation = animation
        self.operation = operation

        self.matrix = {}
        self._setup_matrix()

    def _setup_matrix(self) -> None:
        for timeline in self.animation.timeline.permutations():
            s = timeline.start
            e = timeline.end

            if s not in self.matrix.keys():
                self.matrix[s] = {e: (999999999.0, -1)}
            else:
                self.matrix[s][e] = (999999999.0, -1)

    def _run_calculation_on_timeline(self, timeline):
        s = timeline.start
        e = timeline.end
        frames = self.animation.get_frames(timeline)
        error, index = self.operation.calculate(frames)
        self.matrix[s][e] = (error, index)

    def _execute_operation(self) -> None:
        pool = ThreadPool(4)
        pool.map(self._run_calculation_on_timeline, self.animation.timeline.permutations())
        pool.close()
        pool.join()

    def value_of_max_error(self, timeline: Timeline) -> float:
        assert self.matrix != {}
        s = timeline.start
        e = timeline.end
        return self.matrix[s][e][0]

    def value_of_max_error_for_selection(self, selection: Selection) -> float:
        pairs: List[Tuple[Time, Time]] = selection.get_pairs()
        timelines = [Timeline.from_start_end(a, b) for (a, b) in pairs]
        return max([self.value_of_max_error(timeline) for timeline in timelines])

    def index_of_max_error(self, timeline: Timeline) -> float:
        assert self.matrix != {}
        s = timeline.start
        e = timeline.end
        return self.matrix[s][e][1]

    def as_csv(self) -> List[List[str]]:
        csv = [["i", "j", "max_error_value", "max_error_index"]]
        for timeline in self.animation.timeline.permutations():
            s = timeline.start
            e = timeline.end
            row = ["%d" % s, "%d" % e,
                   "%2.8f" % self.value_of_max_error(timeline),
                   "%d" % self.index_of_max_error(timeline)]
            csv.append(row)
        return csv

    def set(self, timeline: Timeline, error: float, index: int) -> None:
        s = int(timeline.start)
        e = int(timeline.end)
        self.matrix[s][e] = (error, index)

    def save(self, directory: str):
        IO.write_list_of_lists_as_csv("%s/%s-evaluation.csv" % (directory, self.animation.name), self.as_csv())


    @staticmethod
    def _get_data(filepath) -> Tuple[List[Timeline], List[float], List[int]]:
        csv = IO.read_csv_content_as_list_of_lists(filepath)

        data: List[List[float]] = [TransformStringsInList.as_floats(row) for row in csv[1:]]

        timelines = []
        values = []
        indices = []
        for row in data:
            s = int(row[0])
            e = int(row[1])
            timelines.append(Timeline.from_start_end(Time(s), Time(e)))
            values.append(float(row[2]))
            indices.append(int(row[3]))

        return timelines, values, indices

    @staticmethod
    def from_csv(filepath: str, animation: Animation, operation: ErrorMatrixOperation):
        timelines, values, indices = ErrorMatrix._get_data(filepath)
        error_matrix: ErrorMatrix = ErrorMatrix(animation, operation)
        for (timeline, value, index) in zip(timelines, values, indices):
            error_matrix.set(timeline, value, index)
        return error_matrix

    @staticmethod
    def from_animation(animation: Animation, operation: ErrorMatrixOperation):
        error_matrix: ErrorMatrix = ErrorMatrix(animation, operation)
        error_matrix._execute_operation()
        return error_matrix
