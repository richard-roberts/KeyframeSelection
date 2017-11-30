from typing import List

from src.animation.time import Time


class Timeline:
    def __init__(self, start: Time, end: Time):
        self.start = start
        self.end = end

    def as_range(self, increment: Time):
        times: List[Time] = []

        current = self.start
        while current < self.end:
            times.append(current)
            current = current + increment
        times.append(self.end)

        return times

    def number_of_frames(self) -> int:
        n_frames = self.end.time - self.start.time + 1
        assert int(n_frames) == n_frames
        return int(n_frames)

    def permutations(self):
        timelines = []
        s = int(self.start.time)
        e = int(self.end.time)
        for s in range(s, e):
            for e in range(s + 1, e + 1):
                timeline: Timeline = Timeline(Time(s), Time(e))
                timelines.append(timeline)
        return timelines


class CreateTimeline:
    @staticmethod
    def from_times(times: List[Time]) -> Timeline:
        start = times[0]
        end = times[-1]
        return Timeline(start, end)

    @staticmethod
    def from_start_end(start: Time, end: Time) -> Timeline:
        return Timeline(start, end)
