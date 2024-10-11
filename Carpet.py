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
        self.shoot_cd = 0
        self.acceleration = [0, 0]

    def shoot(self, enemy_x: int, enemy_y: int, velocity_x: int, velocity_y: int):
        if self.shoot_cd == 0:
            self.action.attack = [enemy_x + (velocity_x * 0.3), enemy_y + (velocity_y * 0.3)]
        else:
            pass

    def action_to_dict(self):
        result = {
            "acceleration":
                {
                "x": self.action.acceleration[0],
                "y": self.action.acceleration[1]
                },
            "activateShield": self.action.activateShield,
            "attack":
                {
                "x": self.action.attack[0],
                "y": self.action.attack[1]
                },
            "id": self.id
        }
        return json.dumps(result)

    def scan(self):
        pass

    def move(self, x: int, y: int):
        pass




