import json
from time import sleep
from tkinter.constants import ACTIVE
from typing import Optional, List

from config import Config
import requests
from copy import copy


class Action:
    def __init__(self, id: str, acceleration: list[float] = None, activateShield: bool = None, attack: list[int] = None, ):
        self.acceleration = acceleration
        self.activateShield = activateShield
        self.attack = attack
        self.id = id

    def to_dict(self):
        result = {
            "id": self.id
        }
        if self.acceleration is not None:
            result["acceleration"] = {
                "x": self.acceleration[0],
                "y": self.acceleration[1]
            }
        if self.activateShield is not None:
            result["activateShield"] = self.activateShield
        if self.attack is not None:
            result["attack"] = {
                "x": self.attack[0],
                "y": self.attack[1]
            }
        return json.dumps(result)


class Target:
    def __init__(self, carp_x, carp_y):
        self.coordinates = [carp_x, carp_y]  #координаты ковра (нашего)
        self.health = 0
        self.shieldLeftMs = 0
        self.velocity = [0, 0]


class Velocity:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    @classmethod
    def from_dict(cls, data):
        return cls(x=data['x'], y=data['y'])


class Action:
    def __init__(self, id: str):
        self.acceleration = [0, 0]
        self.activateShield = False
        self.attack = [0, 0]
        self.id = id


class Anomaly:
    def __init__(self, id: str, radius: float, strength: float, velocity: Velocity, x: float, y: float, effective_radius: float):
        self.id = id
        self.radius = radius
        self.strength = strength
        self.velocity = velocity
        self.x = x
        self.y = y
        self.effective_radius = effective_radius

    @classmethod
    def from_dict(cls, data):
        velocity = Velocity.from_dict(data['velocity'])
        return cls(
            id=data['id'],
            radius=data['radius'],
            strength=data['strength'],
            velocity=velocity,
            x=data['x'],
            y=data['y'],
            effective_radius=data['effectiveRadius']
        )


class Enemy:
    def __init__(self, health: int, kill_bounty: int, shield_left_ms: int, status: str, velocity: Velocity, x: float, y: float):
        self.health = health
        self.kill_bounty = kill_bounty
        self.shield_left_ms = shield_left_ms
        self.status = status
        self.velocity = velocity
        self.x = x
        self.y = y

    @classmethod
    def from_dict(cls, data):
        velocity = Velocity.from_dict(data['velocity'])
        return cls(
            health=data['health'],
            kill_bounty=data['killBounty'],
            shield_left_ms=data['shieldLeftMs'],
            status=data['status'],
            velocity=velocity,
            x=data['x'],
            y=data['y']
        )


class Transport:
    def __init__(self, id: str, health: int, status: str, velocity: Velocity, x: float, y: float, anomaly_acceleration: Velocity, self_acceleration: Velocity, shield_left_ms: int, attack_cooldown_ms: int, death_count: int, shield_cooldown_ms: int, shield_time_ms: int):
        self.id = id
        self.health = health
        self.status = status
        self.velocity = velocity
        self.x = x
        self.y = y
        self.anomaly_acceleration = anomaly_acceleration
        self.self_acceleration = self_acceleration
        self.shield_left_ms = shield_left_ms
        self.attack_cooldown_ms = attack_cooldown_ms
        self.death_count = death_count
        self.shield_cooldown_ms = shield_cooldown_ms
        self.shield_time_ms = shield_time_ms

    @classmethod
    def from_dict(cls, data):
        velocity = Velocity.from_dict(data['velocity'])
        anomaly_acceleration = Velocity.from_dict(data['anomalyAcceleration'])
        self_acceleration = Velocity.from_dict(data['selfAcceleration'])
        return cls(
            id=data['id'],
            health=data['health'],
            status=data['status'],
            velocity=velocity,
            x=data['x'],
            y=data['y'],
            anomaly_acceleration=anomaly_acceleration,
            self_acceleration=self_acceleration,
            shield_left_ms=data['shieldLeftMs'],
            attack_cooldown_ms=data['attackCooldownMs'],
            death_count=data['deathCount'],
            shield_cooldown_ms=data['shieldCooldownMs'],

        )


class Response:
    def __init__(self, attack_cooldown_ms: int, attack_damage: int, attack_explosion_radius: int, attack_range: int, map_size: Velocity, max_accel: float, max_speed: float, name: str, points: int, revive_timeout_sec: int, transport_radius: float, shield_cooldown_ms: int):
        self.anomalies = []
        self.bounties = []
        self.enemies = []
        self.transports = []
        self.wanted_list = []
        self.attack_cooldown_ms = attack_cooldown_ms
        self.attack_damage = attack_damage
        self.attack_explosion_radius = attack_explosion_radius
        self.attack_range = attack_range
        self.map_size = map_size
        self.max_accel = max_accel
        self.max_speed = max_speed
        self.name = name
        self.points = points
        self.revive_timeout_sec = revive_timeout_sec
        self.transport_radius = transport_radius
        self.shield_cooldown_ms = shield_cooldown_ms

    def predict_next(self) -> 'Response':
        new_response = copy(self)

        for anomaly in new_response.anomalies:
            anomaly.x += anomaly.velocity.x
            anomaly.y += anomaly.velocity.y

        for enemy in new_response.enemies:
            enemy.x += enemy.velocity.x
            enemy.y += enemy.velocity.y
            if enemy.shield_left_ms >= 400:
                enemy.shield_left_ms -= 400
            else:
                enemy.shield_left_ms = 0
            

        for transport in new_response.transports:
            if transport.attack_cooldown_ms >= 400:
                transport.attack_cooldown_ms -= 400
            else:
                transport.attack_cooldown_ms = 0

            if transport.shield_cooldown_ms >= 400:
                transport.shield_cooldown_ms -= 400
            else:
                transport.shield_cooldown_ms = 0
        
            if transport.shield_left_ms >= 400:
                transport.shield_left_ms -= 400
            else:
                transport.shield_left_ms = 0

            transport.x += transport.velocity.x + transport.anomaly_acceleration.x
            transport.y += transport.velocity.y + transport.anomaly_acceleration.y

        for wanted in new_response.wanted_list:
            wanted.x += wanted.velocity.x
            wanted.y += wanted.velocity.y
            if wanted.shield_left_ms >= 400:
                wanted.shield_left_ms -= 400
            else:
                wanted.shield_left_ms = 0

        if new_response.attack_cooldown_ms >= 400:
            new_response.attack_cooldown_ms -= 400
        else:
            new_response.attack_cooldown_ms = 0
 
        if new_response.shield_cooldown_ms >= 400:
            new_response.shield_cooldown_ms -= 400
        else:
            new_response.shield_cooldown_ms = 0
 
        if new_response.shield_time_ms >= 400:
            new_response.shield_time_ms -= 400
        else:
            new_response.shield_time_ms = 0 

        return new_response 

    @classmethod
    def from_dict(cls, data):
        # Создание основного объекта response
        map_size = Velocity.from_dict(data['mapSize'])
        response = cls(
            attack_cooldown_ms=data['attackCooldownMs'],
            attack_damage=data['attackDamage'],
            attack_explosion_radius=data['attackExplosionRadius'],
            attack_range=data['attackRange'],
            map_size=map_size,
            max_accel=data['maxAccel'],
            max_speed=data['maxSpeed'],
            name=data['name'],
            points=data['points'],
            revive_timeout_sec=data['reviveTimeoutSec'],
            transport_radius=data['transportRadius'],
            shield_time_ms=data['shieldTimeMs'],
        )

        # Добавление аномалий
        for anomaly_data in data['anomalies']:
            response.anomalies.append(Anomaly.from_dict(anomaly_data))

        # Добавление врагов
        for enemy_data in data['enemies']:
            response.enemies.append(Enemy.from_dict(enemy_data))

        # Добавление транспорта
        for transport_data in data['transports']:
            response.transports.append(Transport.from_dict(transport_data))

        # Добавление объектов wantedList
        for wanted_data in data['wantedList']:
            response.wanted_list.append(Enemy.from_dict(wanted_data))

        return response

    def get_actions(self):
        actions: List[Action] = []
        for transport in self.transports:
            acceleration = [1, 0]
            activateShield = False
            #ОСТУТСТВУЕТ ЛОГИКА
            if transport.shield_cooldown_ms == 0:
                activateShield = True
            actions.append(Action(transport.id, acceleration, activateShield))
        return actions


class Game:
    def __init__(self):
        self.response: Optional[Response] = None
        self.operations: List[Action] = []

    def new_request(self):
        self.response = Response.from_dict({
  "anomalies": [
    {
      "effectiveRadius": 0,
      "id": "string",
      "radius": 0,
      "strength": 0,
      "velocity": {
        "x": 1.2,
        "y": 1.2
      },
      "x": 1,
      "y": 1
    }
  ],
  "attackCooldownMs": 1000,
  "attackDamage": 10,
  "attackExplosionRadius": 10,
  "attackRange": 10,
  "bounties": [],
  "enemies": [
    {
      "health": 100,
      "killBounty": 10,
      "shieldLeftMs": 5000,
      "status": "alive",
      "velocity": {
        "x": 1.2,
        "y": 1.2
      },
      "x": 1,
      "y": 1
    }
  ],
  "mapSize": {
    "x": 1,
    "y": 1
  },
  "maxAccel": 1,
  "maxSpeed": 10,
  "name": "player1",
  "points": 100,
  "reviveTimeoutSec": 2,
  "shieldCooldownMs": 10000,
  "shieldTimeMs": 5000,
  "transportRadius": 5,
  "transports": [
    {
      "anomalyAcceleration": {
        "x": 1.2,
        "y": 1.2
      },
      "attackCooldownMs": 0,
      "deathCount": 0,
      "health": 100,
      "id": "00000000-0000-0000-0000-000000000000",
      "selfAcceleration": {
        "x": 1.2,
        "y": 1.2
      },
      "shieldCooldownMs": 0,
      "shieldLeftMs": 0,
      "status": "alive",
      "velocity": {
        "x": 1.2,
        "y": 1.2
      },
      "x": 1,
      "y": 1
    }
  ],
  "wantedList": [
    {
      "health": 100,
      "killBounty": 10,
      "shieldLeftMs": 5000,
      "status": "alive",
      "velocity": {
        "x": 1.2,
        "y": 1.2
      },
      "x": 1,
      "y": 1
    }
  ]
})
        # data = [x.to_dict() for x in self.operations]
        # data = {
        #     "transports": data
        # }
        # self.response = Response.from_dict(requests.post(Config.url, json=data, headers={'X-Auth-Token': Config.Token}).json())

    def move(self):
        self.new_request()
        predicted_response = self.response.predict_next()
        self.operations = predicted_response.get_actions()


