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

    def action_to_dict(self):
        return {
            "acceleration": {
                "x": 1.2,
                "y": 1.2
            },
            "activateShield": true,
            "attack": {
                "x": 1,
                "y": 1
            }
        }



    def shoot(self, enemy_x: int, enemy_y: int, velocity_x: int, velocity_y: int):
        if self.shoot_cd == 0:
            self.action.attack = [enemy_x + (velocity_x * 0.3), enemy_y + (velocity_y * 0.3)]
        else:
            pass

    def scan(self):
        pass

    def move(self, x: int, y: int):
        pass




