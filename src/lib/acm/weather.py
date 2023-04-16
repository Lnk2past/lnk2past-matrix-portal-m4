import gc
import time

from adafruit_matrixportal.matrixportal import MatrixPortal

from acm import clear_portal
from acm.colors import RED_COLOR, GREEN_COLOR, BLUE_COLOR, YELLOW_COLOR, WHITE_COLOR


class Weather:
    def __init__(self, matrixportal: MatrixPortal) -> None:
        clear_portal(matrixportal)
        self.update_rate = 60
        self.matrixportal = matrixportal
        self.matrixportal.set_background('images/day.bmp')
        self.matrixportal.add_text(text_position=(2, 6))
        self.matrixportal.add_text(text_position=(2, 16))


    def update(self):
        try:
            data = self.matrixportal.fetch()
            if data['hour'] > 14 or data['hour'] < 7:
                self.matrixportal.set_background('images/night.bmp')
                if data['temp'] < 50.0:
                    temp_color = WHITE_COLOR
                elif data['temp'] < 75.0:
                    temp_color = YELLOW_COLOR
                else:
                    temp_color = RED_COLOR

            elif data['hour'] > 6:
                self.matrixportal.set_background('images/day.bmp')
                if data['temp'] < 50.0:
                    temp_color = GREEN_COLOR
                elif data['temp'] < 75.0:
                    temp_color = YELLOW_COLOR
                else:
                    temp_color = RED_COLOR

            self.matrixportal.set_text(f'{data["hour"]%12:>02}:{data["minute"]:>02}{"am" if data["hour"] < 12 else "pm"}')
            self.matrixportal.set_text_color(temp_color)

            self.matrixportal.set_text(f'{data["temp"]}F', index=1)
            self.matrixportal.set_text_color(temp_color, index=1)

            return time.monotonic()
        except (ValueError, RuntimeError) as e:
            print('Some error occured, retrying! -', e)

    gc.collect()
