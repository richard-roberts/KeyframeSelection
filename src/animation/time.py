class Time:
    def __init__(self, time: float):
        self.time = time

    def __add__(self, other):
        return Time(self.time + other.time)

    def __lt__(self, other):
        return self.time < other.time

    def __gt__(self, other):
        return self.time > other.time
