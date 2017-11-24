from typing import List

from src.scene.things.thing import Thing
from src.scene.coordinates.value import Value
from src.animation.frame import Frame
from src.animation.time import Time
from src.animation.timeline import Timeline
from src.utils import TransformFloatsInList


class Animation:
    def __init__(self, timeline: Timeline, frames: List[Frame]):
        self.timeline = timeline
        self.frames = frames

    def dimensions(self) -> List[str]:
        dimensions = ["time"]
        first_thing: Thing = self.frames[0].things[0]
        for coordinate in first_thing.coordinates:
            for value in coordinate.values:
                dimensions.append(value.name)
        return dimensions

    def value_matrix(self) -> List[List[float]]:
        matrix = []

        times = self.timeline.as_range(Time(1.0))
        for (time, frame) in zip(times, self.frames):
            values: List[Value] = []
            first_thing: Thing = frame.things[0]
            for coordinate in first_thing.coordinates:
                values += coordinate.values

            row = [item.value for item in values]
            row_with_time = [time.time] + row
            matrix.append(row_with_time)

        return matrix

    def as_csv(self) -> List[List[str]]:
        dimensions: List[str] = self.dimensions()
        data: List[List[str]] = [TransformFloatsInList.asStrings(row) for row in self.value_matrix()]
        return [dimensions] + data
