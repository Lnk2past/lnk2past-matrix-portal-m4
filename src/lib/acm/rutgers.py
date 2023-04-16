from adafruit_matrixportal.matrixportal import MatrixPortal

from acm import clear_portal


class RUC:
    def __init__(self, matrixportal: MatrixPortal) -> None:
        clear_portal(matrixportal)
        self.update_rate = 0.05
        self.matrixportal = matrixportal
        matrixportal.add_text(text_position=(0, 15), text_color=0xff0000, scrolling=True)
        matrixportal.set_text('Rutgers Camden Hackathon!\nApril 15 2023!')

    def update(self) -> None:
        self.matrixportal.scroll()
