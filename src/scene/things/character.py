from typing import List

from SalientPosesReference.src.scene.coordinates.coordinate import Coordinate
from SalientPosesReference.src.scene.meshes.mesh import Mesh
from SalientPosesReference.src.scene.things.thing import Thing


class Character(Thing):
    def __init__(self, location: Coordinate, meshes: List[Mesh], coordinates: List[Coordinate]):
        super().__init__(location, meshes, coordinates)
