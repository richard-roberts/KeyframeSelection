from typing import List

from src.scene.coordinates.coordinate import Coordinate
from src.scene.meshes.mesh import Mesh


class Thing:
    def __init__(self, location: Coordinate, meshes: List[Mesh], coordinates: List[Coordinate]):
        self.location = location
        self.meshes = meshes
        self.coordinates = coordinates
