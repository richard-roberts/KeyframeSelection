import os
import time

from src.analysis.error_table import ErrorTable
from src.animation.animation import Animation
from src.selection.selection import Selection
from src.utils import IO, TransformFloatsInList


class Selector:
    def __init__(self, name: str, animation: Animation, error_table: ErrorTable):
        self.name = name
        self.animation = animation
        self.error_table = error_table
        self.selections = []
        self.times = []

        self.total_frames = self.animation.timeline.number_of_frames()
        self.previous = Selection.first_selection(self.animation.timeline)

    def compute(self):
        raise NotImplementedError

    def execute(self, iterations=-1):
        if iterations == -1:
            iterations = self.animation.get_n_frames() - 2
        assert self.error_table is not None

        for _ in range(iterations):
            start = time.time()
            self.compute()
            end = time.time()
            micro_exe_time = int((end - start) * 1000 * 1000)
            self.times.append(micro_exe_time)

    def as_csv(self, include_timer: bool):
        header = ["n_keyframes", "error"]
        if include_timer:
            header = ["exe_time"] + header

        max_keyframes = -1
        content = []
        for (exe_time, selection) in zip(self.times, self.selections):
            error = self.error_table.value_of_max_error_for_selection(selection)
            keyframes = selection.get()
            if len(keyframes) > max_keyframes:
                max_keyframes = len(keyframes)
            row = [len(keyframes), str(error)] + TransformFloatsInList.as_strings(keyframes)

            if include_timer:
                row = [exe_time] + row
            content.append(row)

        for i in range(max_keyframes):
            keyframe_name = "k%d" % (i + 1)
            header.append(keyframe_name)

        return [header] + content

    def save(self, directory: str, include_timer: bool):
        IO.write_list_of_lists_as_csv("%s/%s-%s.csv" % (directory, self.animation.name, self.name),
                                      self.as_csv(include_timer))

    @staticmethod
    def from_file(filepath: str, animation: Animation):
        csv = IO.read_csv_content_as_list_of_lists(filepath)

        selector = Selector(os.path.basename(filepath), animation, None)
        for row in csv[1:]:
            selected = [int(v) for v in row[2:]]
            selection: Selection = Selection.first_selection(animation.timeline)
            selection.add(*selected[1:-1])

            selector.selections.append(selection)

        return selector
