from typing import List, Tuple

from SalientPosesReference.src.animation.timeline import Timeline
from SalientPosesReference.src.types import Time


class Selection:
    def __init__(self, timeline: Timeline) -> None:
        self.timeline = timeline
        self.keyframes: List[bool] = [True] + [False for _ in range(timeline.start + 1, timeline.end)] + [True]
        self._n_frames = self.timeline.number_of_frames()

    def add(self, *times) -> None:
        for time in times:
            index = self.timeline.time_to_index(time)
            self.keyframes[index] = True

    def add_with_error_on_duplicate(self, time: Time) -> None:
        index = self.timeline.time_to_index(time)
        assert self.keyframes[index] is not True
        self.keyframes[index] = True

    def get(self) -> List[Time]:
        return [self.timeline.index_to_time(index) for index, isKeyframe in enumerate(self.keyframes) if isKeyframe]

    def first(self) -> Time:
        index = 0
        while not self.keyframes[index]:
            index += 1
        return self.timeline.index_to_time(index)

    def last(self) -> Time:
        index = len(self.keyframes) - 1
        while not self.keyframes[index]:
            index -= 1
        return self.timeline.index_to_time(index)

    def get_pairs(self) -> List[Tuple[Time, Time]]:
        keys = self.get()
        return list(zip(keys[:-1], keys[1:]))

    def n_keyframes(self) -> int:
        return len(self.get())

    def as_zero_indexed_integers(self) -> List[int]:
        return [i - self.timeline.start for i in self.get()]

    def as_binary(self) -> List[int]:
        return [1 if value else 0 for value in self.keyframes]

    def compression(self) -> float:
        return 1 - (self.n_keyframes() / self._n_frames)

    def __str__(self):
        times = self.get()

        ret: str = "Selection["
        for time in times[:-1]:
            ret += "%2.2f, " % time
        ret += "%2.2f]" % times[-1]
        return ret

    @staticmethod
    def first_selection(timeline: Timeline):
        selection = Selection(timeline)
        selection.add(timeline.start)
        selection.add(timeline.end)
        return selection

    @staticmethod
    def as_copy(timeline: Timeline, other):
        selection = Selection(timeline)
        for time in other.get():
            selection.add(time)
        return selection
