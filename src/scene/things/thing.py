from typing import List

from SalientPosesReference.src.scene.coordinates.coordinate import Coordinate
from SalientPosesReference.src.scene.meshes.mesh import Mesh


class Thing:
    def __init__(self, location: Coordinate, meshes: List[Mesh], coordinates: List[Coordinate]):
        self.location = location
        self.meshes = meshes
        self.coordinates = coordinates

    def as_point(self):
        point = []
        for coordinate in self.coordinates:
            point += coordinate.as_point()
        return point
