import numpy as np
from settings import Settings


class Page:
    def __init__(self, index: int, settings: Settings):
        self.index = index
        self.content = self.get_blank_page(settings)
        self.saved_on_disk = False

    def get_blank_page(self, settings):
        crop_height = settings.crop_height_cords[1] - settings.crop_height_cords[0]
        shape = (crop_height * settings.amount_of_rows, settings.video_width * 2, 3)
        return np.full(shape, 255)

