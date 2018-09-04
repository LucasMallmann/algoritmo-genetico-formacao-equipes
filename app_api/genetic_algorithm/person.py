import random
import json


class Person(object):
    def __init__(self, name: str):
        self.name = name
        self.p1 = random.uniform(0, 10)
        self.p2 = random.uniform(0, 10)
        self.p3 = random.uniform(0, 10)
