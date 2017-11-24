from typing import List

from src.scene.things.thing import Thing


class Frame:
    def __init__(self, things: List[Thing]):
        self.things = things
