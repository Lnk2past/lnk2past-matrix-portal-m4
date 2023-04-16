import gc
import time
import board
from adafruit_matrixportal.matrixportal import MatrixPortal
from digitalio import DigitalInOut, Direction, Pull

from acm import MODES, MODE_FUNCS

DATA_SOURCE = 'http://192.168.1.159:5000/'

UP_BUTTON = DigitalInOut(board.BUTTON_UP)
UP_BUTTON.direction = Direction.INPUT
UP_BUTTON.pull = Pull.UP

DOWN_BUTTON = DigitalInOut(board.BUTTON_DOWN)
DOWN_BUTTON.direction = Direction.INPUT
DOWN_BUTTON.pull = Pull.UP

matrixportal = MatrixPortal(
    url=DATA_SOURCE,
    status_neopixel=board.NEOPIXEL,
    bit_depth=6,
    json_path=['data']
)

last_check = None
mode = 'rutgers'
MODE = MODE_FUNCS[mode](matrixportal)

last_check = None
while True:
    if not UP_BUTTON.value:
        while not UP_BUTTON.value:
            pass
        mode = MODES[(MODES.index(mode)+1) % len(MODES)]
        MODE = MODE_FUNCS[mode](matrixportal)

    if last_check is None or time.monotonic() > last_check + MODE.update_rate:
        MODE.update()
        last_check = time.monotonic()
