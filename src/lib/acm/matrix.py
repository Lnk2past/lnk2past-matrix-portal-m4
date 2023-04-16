import gc
import random

import board
import displayio
import adafruit_lis3dh
from adafruit_matrixportal.matrixportal import MatrixPortal

from acm.colors import build_palette, PALETTES
from acm import clear_portal


class CodeDrop:
    def __init__(self, start_row = 0):
        self.x = random.randint(0, 63)
        self.y = start_row
        self.range = random.randint(2,9)
        self.speed = random.choice([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 3]) * (-1 if start_row else 1)
        self.orientation = -1 if start_row else 1

    def update(self, sprite):
        for y in range(self.range):
            yp = self.y - y * self.orientation
            if yp > -1 and yp < 32:
                sprite[self.x + yp * 64] = self.range - y - 1
        self.y += self.speed

    def flip(self):
        self.speed *= -1
        self.orientation *= -1

class CodeRain:
    def __init__(self, matrixportal: MatrixPortal) -> None:
        clear_portal(matrixportal)
        self.update_rate = 0.01
        self.matrixportal = matrixportal
        color_bitmap = displayio.Bitmap(64, 32, 9)
        color_palette = build_palette(PALETTES['matrix'])
        sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
        matrixportal.graphics._bg_group.append(sprite)

        self.i2c = board.I2C()  # uses board.SCL and board.SDA
        self.lis3dh = adafruit_lis3dh.LIS3DH_I2C(self.i2c, address=0x19)
        self.lis3dh.range = adafruit_lis3dh.RANGE_2_G
        self.start_row = 0

        self.code_drops = []

    def update(self) -> None:
        # print(gc.mem_free())
        x, y, z = [
            value / adafruit_lis3dh.STANDARD_GRAVITY for value in self.lis3dh.acceleration
        ]
        if (y < 0 and self.start_row == 0) or (y > 0 and self.start_row == 31):
            self.start_row = 0 if self.start_row else 31
            for drop in self.code_drops:
                drop.flip()

        color_bitmap = displayio.Bitmap(64, 32, 9)
        for _ in range(8):
            self.code_drops.append(CodeDrop(self.start_row))
        rem = []
        for i in range(len(self.code_drops)):
            drop = self.code_drops[i]
            drop.update(color_bitmap)
            if drop.y >= 39 or drop.y <= -8:
                rem.append(i)
        for r in reversed(rem):
            del self.code_drops[r]
        self.matrixportal.graphics._bg_group[0].bitmap = color_bitmap
        gc.collect()
