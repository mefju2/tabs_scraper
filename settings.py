from dataclasses import dataclass


@dataclass
class Settings:
    crop_height_cords: tuple
    measure_number_height_cords: tuple
    measure_number_width_cords: tuple
    amount_of_rows: int
