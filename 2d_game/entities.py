import math, random
import pyglet
from DIPPID import SensorUDP

from constants import (FPS, WIDTH, HEIGHT, SPEED_PER_SEGMENT,BASE_SPEED, GOLD_LIFETIME,
                       PORT)
from resources import (game_batch, head_img, body_img, coin_img,
                       gold_img, SEG_SPACING)

class RectObj:
    def __init__(self, img):
        self.sprite = pyglet.sprite.Sprite(img, batch=game_batch)
        self.SnakeAngle = SnakeAngle()
    def step(self):
        self.sprite.x += self.SnakeAngle.x / FPS
        self.sprite.y += self.SnakeAngle.y / FPS

class SnakeHead(RectObj, SensorUDP):
    def __init__(self, x, y):
        RectObj.__init__(self, head_img)
        SensorUDP.__init__(self, PORT)
        self.sprite.x, self.sprite.y = x, y
        self.angle  = 0       
        self.target = 0        
        self.segment_count = 0 
        self.register_callback("gravity", self._tilt_cb)

    def _tilt_cb(self, data):
        if "x" in data and "z" in data:
            self.target = math.atan2(-data["x"], data["z"])

    def _keep_inside(self):
        half_w, half_h = self.sprite.width / 2, self.sprite.height / 2
        self.sprite.x = min(max(half_w, self.sprite.x), WIDTH  - half_w)
        self.sprite.y = min(max(half_h, self.sprite.y), HEIGHT - half_h)

    def step(self):
        diff = (self.target - self.angle + math.pi) % (2*math.pi) - math.pi
        self.angle += diff * 0.07

        speed = BASE_SPEED + self.segment_count * SPEED_PER_SEGMENT
        self.SnakeAngle = SnakeAngle(math.sin(self.angle)*speed,
                                     math.cos(self.angle)*speed)
        super().step()
        self._keep_inside()
        self.sprite.rotation = -math.degrees(
            math.atan2(self.SnakeAngle.y, self.SnakeAngle.x)
        )

class Segment(RectObj):
    def __init__(self):
        self.timeAlive=0
        super().__init__(body_img)

class Coin(RectObj):
    def __init__(self, golden=False):
        super().__init__(gold_img if golden else coin_img)
        self.golden = golden
        self.timer  = GOLD_LIFETIME if golden else None
        self.phase  = random.random() * math.tau
        self.respawn()

    def respawn(self):
        hw, hh = self.sprite.width // 2, self.sprite.height // 2
        self.sprite.x = random.randint(hw, WIDTH  - hw)
        self.sprite.y = random.randint(hh, HEIGHT - hh)

    def step(self, dt):
        self.phase += dt * 6
        if self.golden:
            self.sprite.scale   = 1 + 0.1 * math.sin(self.phase)
            self.sprite.opacity = int(200 + 55 * math.sin(self.phase*1.5))
        else:
            self.sprite.y += math.sin(self.phase) * 0.3
        if self.timer is not None:
            self.timer -= dt

    def expired(self):
        return self.golden and self.timer is not None and self.timer <= 0

class SnakeAngle:
    def __init__(self, x=0, y=0):
        self.x, self.y = x, y

def overlap(a, b, padding):

    ax = a.sprite.x - a.sprite.width  / 2 - padding
    ay = a.sprite.y - a.sprite.height / 2 - padding
    aw = a.sprite.width  + 2 * padding
    ah = a.sprite.height + 2 * padding

    bx = b.sprite.x - b.sprite.width  / 2 - padding
    by = b.sprite.y - b.sprite.height / 2 - padding
    bw = b.sprite.width  + 2 * padding
    bh = b.sprite.height + 2 * padding

    return (
        ax < bx + bw and
        ax + aw > bx and
        ay < by + bh and
        ay + ah > by
    )
