import json
from Config import Config
import requests


class Velocity:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    @classmethod
    def from_dict(cls, data):
        return cls(x=data['x'], y=data['y'])


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
    def __init__(self, id: str, health: int, status: str, velocity: Velocity, x: float, y: float, anomaly_acceleration: Velocity, self_acceleration: Velocity, shield_left_ms: int, attack_cooldown_ms: int, death_count: int):
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
            death_count=data['deathCount']
        )


class Response:
    def __init__(self, attack_cooldown_ms: int, attack_damage: int, attack_explosion_radius: int, attack_range: int, map_size: Velocity, max_accel: float, max_speed: float, name: str, points: int, revive_timeout_sec: int, shield_cooldown_ms: int, shield_time_ms: int, transport_radius: float):
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
        self.shield_cooldown_ms = shield_cooldown_ms
        self.shield_time_ms = shield_time_ms
        self.transport_radius = transport_radius

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
            shield_cooldown_ms=data['shieldCooldownMs'],
            shield_time_ms=data['shieldTimeMs'],
            transport_radius=data['transportRadius']
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


class Scanner(object):
    def __init__(self):
        self.response = None

    def get_response(self):
        request = requests.get(Config.url)
        self.response = Response.from_dict(request.json())

    def choose_enemy(self):
        pass
