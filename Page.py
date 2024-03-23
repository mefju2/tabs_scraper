from dataclasses import dataclass

import numpy as np
from numpy import ndarray


class Page:
    def __init__(self, index: int, page_height: int):
        self.index = index
        self.content = self.get_blank_page(page_height)
        self.saved_on_disk = False

    def get_blank_page(self, page_height):
        shape = (page_height, 2560, 3)
        return np.full(shape, 255)

