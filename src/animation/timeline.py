from typing import List

from src.types import Time


class Timeline:
    def __init__(self, start: Time, end: Time):
        self.start = start
        self.end = end

    def time_to_index(self, time: Time) -> int:
        return time - self.start

    def index_to_time(self, index: int) -> Time:
        return index + self.start

    def as_range(self) -> List[Time]:
        return list(range(self.start, self.end + 1))

    def number_of_frames(self) -> int:
        n_frames = self.end - self.start + 1
        assert int(n_frames) == n_frames
        return int(n_frames)

    def permutations(self):
        timelines = []
        s = int(self.start)
        e = int(self.end)
        for s in range(s, e):
            for e in range(s + 1, e + 1):
                timeline: Timeline = Timeline(s, e)
                timelines.append(timeline)
        return timelines

    @staticmethod
    def from_times(times: List[Time]):
        start = times[0]
        end = times[-1]
        return Timeline(start, end)

    @staticmethod
    def from_start_end(start: Time, end: Time):
        return Timeline(start, end)
