from typing import List

from src.scene.things.thing import Thing
from src.animation.time import Time


class Frame:
    def __init__(self, time: Time, things: List[Thing]):
        self.time = time
        self.things = things

    def as_point(self):
        point = [self.time.time]
        for thing in self.things:
            point += thing.as_point()
        return point
