import math, random, sys, pyglet

from constants import (WIDTH, HEIGHT, FPS, NEW_COIN_CHANCE,
                       MAX_COINS)
from resources  import (bg_img, game_batch, ui_batch, coin_sound,
                        death_sound, music_player)
from entities   import SnakeHead, Segment, Coin, overlap

class Game(pyglet.window.Window):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, "Snake")
        self.bg   = pyglet.sprite.Sprite(bg_img, x=0, y=0)
        self.head = SnakeHead(WIDTH/2, HEIGHT/2)
        self.coins, self.segments = [], []
        self.score  = 0
        self.growth = 0
        self.elapsed = 0.0

        self.score_lbl = pyglet.text.Label("0",
            x=self.width//2, y=self.height-50,
            font_size=40, anchor_x="center", anchor_y="center",
            batch=ui_batch)

        self.info_lbl = pyglet.text.Label("0.00 coins/min",
            x=self.width//2, y=self.height-95,
            font_size=20, anchor_x="center", anchor_y="center",
            batch=ui_batch)

        pyglet.clock.schedule_interval(self.update, 1/FPS)
        music_player.play()
        self._spawn_coin()

    def _spawn_coin(self):
        from constants import GOLD_CHANCE
        self.coins.append(Coin(random.random() < GOLD_CHANCE))

    def _reset(self):
        death_sound.play()
        self.segments.clear()
        self.head.sprite.x, self.head.sprite.y = WIDTH/2, HEIGHT/2
        self.head.angle = self.head.target = 0
        self.head.segment_count = 0
        self.score = self.growth = self.elapsed = 0
        self.coins.clear()
        self._spawn_coin()

    def update(self, dt):
        self.elapsed += dt

        if len(self.coins) < MAX_COINS and random.random() < NEW_COIN_CHANCE:
            self._spawn_coin()

        self.head.segment_count = len(self.segments)
        self.head.step()

        for coin in self.coins[:]:
            coin.step(dt)
            if overlap(self.head, coin,0):
                coin_sound.play()
                gain = 3 if coin.golden else 1
                self.score  += gain
                self.growth += gain
                self.coins.remove(coin)
                continue
            if coin.expired():
                self.coins.remove(coin)

        if self.growth > 0:
            seg = Segment()
            seg.sprite.x, seg.sprite.y = self.head.sprite.x, self.head.sprite.y
            self.segments.append(seg)
            self.growth -= 1

        from constants import FOLLOW_SPEED
        from resources import SEG_SPACING
        for i, seg in enumerate(self.segments):
            seg.timeAlive+=1
            if i == 0:
                px, py = self.head.sprite.x, self.head.sprite.y
            else:
                px, py = self.segments[i-1].sprite.x, self.segments[i-1].sprite.y

            dx, dy = px - seg.sprite.x, py - seg.sprite.y
            dist   = math.hypot(dx, dy)
            if dist > SEG_SPACING:
                step = min(dist-SEG_SPACING, FOLLOW_SPEED*dt*(dist-SEG_SPACING))
                seg.sprite.x += dx/dist * step
                seg.sprite.y += dy/dist * step
            seg.sprite.rotation = -math.degrees(math.atan2(dy, dx))

        for seg in self.segments[2:]:
            if overlap(self.head, seg, -20):
                if seg.timeAlive>30:
                    self._reset()
                    break

        self.score_lbl.text = str(self.score)
        mins = self.elapsed/60 if self.elapsed else 1
        self.info_lbl.text = f"{self.score/mins:.2f} coins/min"

    def on_draw(self):
        self.clear()
        self.bg.draw()
        game_batch.draw()
        ui_batch.draw()
    def on_close(self):
        pyglet.app.exit()
        sys.exit()

if __name__ == "__main__":
    Game()
    pyglet.app.run()
