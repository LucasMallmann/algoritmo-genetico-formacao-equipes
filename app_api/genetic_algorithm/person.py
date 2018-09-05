import random
import json


class Person(object):
    def __init__(self, name: str, person_id: int, group_id: int):
        self.name = name
        self.person_id = person_id
        self.group_id = group_id
        self.p1 = random.uniform(0, 10)
        self.p2 = random.uniform(0, 10)
        self.p3 = random.uniform(0, 10)

    def __str__(self):
        return 'Person with name = %s, id = %s and group_id = %s' \
               % (self.name, self.person_id, self.group_id)
