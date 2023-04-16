import gc
import random

import displayio
from adafruit_matrixportal.matrixportal import MatrixPortal

from acm.colors import build_palette, PALETTES
from acm import clear_portal


class GameOfLife:
    def __init__(self, matrixportal: MatrixPortal) -> None:
        clear_portal(matrixportal)
        self.update_rate = 0.05
        self.matrixportal = matrixportal
        color_bitmap = displayio.Bitmap(64, 32, 10)
        color_palette = build_palette(PALETTES['fire'], additional_offset=1)
        sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
        matrixportal.graphics._bg_group.append(sprite)
        for _ in range(1024):
            color_bitmap[random.randint(0, 63), random.randint(0, 31)] = 2

    def update(self) -> None:
        next_color_bitmap = displayio.Bitmap(64, 32, 10)
        bitmap = self.matrixportal.graphics._bg_group[0].bitmap
        for p in range(2048):
            i = p % 64
            j = p // 64
            L = i > 0
            R = i < 63
            U = j > 0
            D = j < 31
            n = (
                (L and       bitmap[i-1 + 64 * (j)] != 0)
                + (L and U and bitmap[i-1 + 64 * (j-1)] != 0)
                + (L and D and bitmap[i-1 + 64 * (j+1)] != 0)
                + (R and       bitmap[i+1 + 64 * (j)] != 0)
                + (R and U and bitmap[i+1 + 64 * (j-1)] != 0)
                + (R and D and bitmap[i+1 + 64 * (j+1)] != 0)
                + (U and       bitmap[i + 64 * (j-1)] != 0)
                + (D and       bitmap[i + 64 * (j+1)] != 0)
            )

            if bitmap[i + 64 * j] != 0 and (n < 2 or n > 3):
                next_color_bitmap[i + 64 * j] = 0
            elif bitmap[i + 64 * j] != 0:
                next_color_bitmap[i + 64 * j] = min(9, bitmap[i + 64 * j] + 1)
            elif n == 3:
                next_color_bitmap[i + 64 * j] = 2
            else:
                next_color_bitmap[i + 64 * j] = bitmap[i + 64 * j]

        if random.randint(1,100) < 5: # 5% chance to MUTATE and reset
            for _ in range(128):
                i = random.randint(0, 63)
                j = random.randint(0, 31)
                next_color_bitmap[i, j] = max(1, bitmap[i + 64 * j])
            color_palette = build_palette(random.choice(list(PALETTES.values())), additional_offset=1)
            sprite = displayio.TileGrid(next_color_bitmap, pixel_shader=color_palette, x=0, y=0)
            self.matrixportal.graphics._bg_group.pop()
            self.matrixportal.graphics._bg_group.append(sprite)
        else:
            self.matrixportal.graphics._bg_group[0].bitmap = next_color_bitmap
