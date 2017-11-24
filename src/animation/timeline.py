from typing import List

from src.animation.time import Time


class Timeline:
    def __init__(self, start: Time, end: Time, fps: int):
        self.start = start
        self.end = end
        self.fps = fps


class CreateTimeline:
    @staticmethod
    def from_times(times: List[Time], fps: int) -> Timeline:
        start = times[0]
        end = times[-1]
        return Timeline(start, end, fps)
