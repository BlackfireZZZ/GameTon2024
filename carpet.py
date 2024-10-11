import json
from math import sqrt
from typing import List


class Action(object):
    def __init__(self, id: str):
        self.acceleration = [0, 0]
        self.activateShield = False
        self.attack = [0, 0]
        self.id = id


class Target(object):
    def __init__(self, carp_x, carp_y):
        self.coordinates = [carp_x, carp_y]  #координаты ковра (нашего)
        self.health = 0
        self.shieldLeftMs = 0
        self.velocity = [0, 0]


class Carpet(object):
    targets: List[Target] = []

    def __init__(self, id: str):
        self.coords = [0, 0]
        self.id = id
        self.action = Action(id)
        self.shoot_cd = 0
        self.acceleration = [0, 0]

    def shoot(self, enemy_x: int, enemy_y: int, velocity_x: int, velocity_y: int):
        if self.shoot_cd == 0:
            self.action.attack = [enemy_x + (velocity_x * 0.4), enemy_y + (velocity_y * 0.4)]
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
        # Главная логика здесь
        pass

    def move(self, x: int, y: int, max_speed: int):
        # 1) разделить вектор движения на три этапа: ускорение, крейсерское движение и торможение
        dist = sqrt(x ** 2 + y ** 2) # модуль вектора расстояния
        movement_vector = [x - self.coords[0], y - self.coords[1]]
        
            

        # now = self.coords
        # want = [x, y]
        # movement_vector = [want[0] - now[0], want[1] - now[1]] #вектор передвижения
        # movement_len = sqrt(movement_vector[0] ** 2 + movement_vector[1] ** 2) 
        # if movement_len <= 10:  #если нам пора замедляться то отрицательное ускорение
        #     self.acceleration = -1 * movement_len
        #     return
        # elif movement_len == 0:   #если мы на месте то ускорение 0
        #     self.acceleration = 0
        #     return
        # k = 10 / movement_len  #кэф масштабирования ускорения
        # acc_vector = [movement_vector[0] * k, movement_vector[1] * k]  #вектор который пройдем за тик/секунду
        # self.acceleration = acc_vector
