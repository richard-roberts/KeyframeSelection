from typing import List

from src.animation.frame import Frame
from src.animation.timeline import Timeline


class Animation:
    def __init__(self, timeline: Timeline, frames: List[Frame]):
        self.timeline = timeline
        self.frames = frames
