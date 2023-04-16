import displayio


RED_COLOR = 0xAA0000
GREEN_COLOR = 0x00AA00
BLUE_COLOR = 0x0000AA
YELLOW_COLOR = 0xAAAA00
WHITE_COLOR = 0xAAAAAA

PALETTES = {
    'bgy': [0x000c7c, 0x0021b0, 0x0046b8, 0x006b96, 0x1b8e61, 0x31b01c, 0x36d119, 0x9de81c],
    'fire': [0x000000, 0x4a0000, 0x7d0200, 0xb40500, 0xed1400, 0xfe6800, 0xffa601, 0xffda09],
    'rainbow': [0x0034f8, 0x00729d, 0x3e944d, 0x6aaf0f, 0xb5c11b, 0xf6cc24, 0xffa212, 0xff7100],
    'matrix': [0x001100, 0x003300, 0x005500, 0x007700, 0x009900, 0x00bb00, 0x00dd00, 0xaaffaa]
}

def build_palette(palette: list[int], additional_offset: int = 0) -> displayio.Palette:
    color_palette = displayio.Palette(len(palette)+1+additional_offset)
    for i,c in enumerate(palette, 1+additional_offset):
        color_palette[i] = c
    return color_palette
