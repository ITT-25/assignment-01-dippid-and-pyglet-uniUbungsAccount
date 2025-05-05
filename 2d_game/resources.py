import os
import pyglet

from constants import ASSET_DIR

game_batch = pyglet.graphics.Batch()
ui_batch   = pyglet.graphics.Batch()

head_img = pyglet.image.load(os.path.join(ASSET_DIR, "snakehead.png")) 
head_img.anchor_x = head_img.width // 2
head_img.anchor_y = head_img.height // 2

body_img = pyglet.image.load(os.path.join(ASSET_DIR, "snakebody.png"))
body_img.anchor_x = body_img.width // 2
body_img.anchor_y = body_img.height // 2

coin_img = pyglet.image.load(os.path.join(ASSET_DIR, "coin.png")) #egg.png
coin_img.anchor_x = coin_img.width // 2
coin_img.anchor_y = coin_img.height // 2

gold_img = pyglet.image.load(os.path.join(ASSET_DIR, "goldcoin.png"))
gold_img.anchor_x = gold_img.width // 2
gold_img.anchor_y = gold_img.height // 2

bg_img = pyglet.image.load(os.path.join(ASSET_DIR, "boardbackground.png"))

coin_sound  = pyglet.media.load(os.path.join(ASSET_DIR, "coincollected.ogg"), streaming=False)
death_sound = pyglet.media.load(os.path.join(ASSET_DIR, "death.ogg"),           streaming=False)

music_player = pyglet.media.Player()
music_player.loop = True
music_player.queue(pyglet.media.load(os.path.join(ASSET_DIR, "backgroundmusic.ogg"), streaming=False))

HEAD_SIZE  = head_img.width
BODY_SIZE  = body_img.width
SEG_SPACING = (HEAD_SIZE + BODY_SIZE) * 0.31
