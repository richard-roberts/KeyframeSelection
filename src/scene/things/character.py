from typing import List

from src.scene.coordinates.coordinate import Coordinate
from src.scene.meshes.mesh import Mesh
from src.scene.things.thing import Thing


class Character(Thing):
    def __init__(self, location: Coordinate, meshes: List[Mesh], coordinates: List[Coordinate]):
        super().__init__(location, meshes, coordinates)
