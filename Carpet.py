import json

class Action(object):
    acceleration = [0, 0]
    activateShield = False
    attack = [0, 0]

    def __init__(self, id: str):
        self.id = id


class Carpet(object):
    def __init__(self, id: str):
        self.id = id
        self.action = Action(id)

    def action_to_dict(self):
        return



    def shoot(self, x: int, y: int, velocity_x: int, velocity_y: int):
        pass

    def scan(self):
        pass

    def move(self, x: int, y: int):
        pass




