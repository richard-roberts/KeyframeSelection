from typing import List, Tuple

from src.animation.animation import Animation
from src.animation.frame import Frame
from src.animation.time import Time
from src.animation.timeline import CreateTimeline
from src.scene.coordinates.coordinate import Coordinate
from src.scene.coordinates.value import Value
from src.scene.things.thing import Thing
from src.utils import IO, TransformStringsInList


class CreateAnimation:
    @staticmethod
    def _get_data(filepath) -> Tuple[List[Time], List[List[Value]]]:
        csv = IO.read_csv_content_as_list_of_lists(filepath)

        dimensions: List[str] = csv[0]
        data: List[List[float]] = [TransformStringsInList.as_floats(row) for row in csv[1:]]

        times = []
        values = []
        for row in data:
            assert dimensions[0] == "time"
            times.append(Time(row[0]))
            values.append([Value(name, value) for (name, value) in zip(dimensions[1:], row[1:])])

        return times, values

    @staticmethod
    def _organise_values_into_coordinates(coordinate_class, values: List[Value]) -> List[Coordinate]:
        coordinates = []

        last_value_name = values[0].name
        sublist_of_values = []
        for value in values:
            curr_value_name = value.name
            if last_value_name.split("-")[0] != curr_value_name.split("-")[0]:
                coordinate: Coordinate = coordinate_class(sublist_of_values)
                coordinates.append(coordinate)
                sublist_of_values = []
            sublist_of_values.append(value)

        # Put in the last coordinate
        if sublist_of_values:
            coordinate: Coordinate = coordinate_class(sublist_of_values)
            coordinates.append(coordinate)

        return coordinates

    @staticmethod
    def _construct_thing_from_values(thing_class, coordinate_class, values: List[Value]) -> Thing:
        coordinates = CreateAnimation._organise_values_into_coordinates(coordinate_class, values)
        return thing_class(None, [], coordinates)

    @staticmethod
    def from_csv(filepath: str, thing_class, coordinate_class) -> Animation:
        times, values = CreateAnimation._get_data(filepath)

        timeline = CreateTimeline.from_times(times, 120)

        frames: List[Frame] = []
        for (time, value) in zip(times, values):
            thing = CreateAnimation._construct_thing_from_values(thing_class, coordinate_class, value)
            frame = Frame([thing])
            frames.append(frame)

        animation = Animation(timeline, frames)
        return animation
