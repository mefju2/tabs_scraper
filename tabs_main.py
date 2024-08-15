import os

import MeasuresService
import PagesService
import TrimService
from settings import Settings


def run():
    os.makedirs("pages", exist_ok=True)
    os.makedirs("measures", exist_ok=True)

    # sky_guitar_settings = Settings((400, 720), (430, 460), (45, 80), 6)
    sky_guitar_settings = Settings((400, 720), (450, 480), (45, 78), 5, 1280, 720)
    sky_guitar_settings_fhd_tabs_up = Settings((0, 500), (56, 88), (80, 110), 5, 1920, 1080)
    sky_guitar_settings_fhd_tabs_down = Settings((600, 1080), (658, 688), (88, 122), 5, 1920, 1080)
    smile_guitar_settings = Settings((645, 1080), (650, 685), (0, 25), 6, 1920, 1080)
    sky_guitar_settings_small = Settings((0, 168), (24, 40), (26, 42), 5, 640, 360)
    kenneth_guitar_settings = Settings((800, 1080), (585, 635), (180, 230), 5, 1600, 1080)
    piano_settings = Settings((0, 255), (0, 25), (110, 150), 5, 1280, 720)
    # extractImagesVertical("The Entertainer.mp4", out_path, 14)
    # extract_images_vertical("Married_Life.mp4", out_path, 10, sky_guitar_settings, (230,))
    # extract_images_vertical("SPRING DAY, CHERRY BLOSSOMS.mp4", out_path, 4, piano_settings)
    # extract_images_vertical("KISS THE RAIN.mp4", out_path, 8, Settings((0, 220), (0, 32), (78, 110), 6), (64, 160))
    # extract_images_vertical("Interstellar.mp4", out_path, 8, Settings((0, 220), (0, 32), (78, 110), 6), (64, 160))
    # extract_images_vertical("ALWAYS WITH ME.mp4", out_path, 3, Settings((0, 220), (0, 32), (78, 110), 6), (64, 160))
    # extract_images_vertical("Interstellar_guitar.mp4", out_path, 7, kenneth_guitar_settings)
    # extract_images_vertical("Kiss the Rain - Guitar Lesson.mp4", out_path, 8, sky_guitar_settings)

    # split_video_into_separate_measures("(Chopin) Nocturne Op.9, No.2 - Guitar.mp4", sky_guitar_settings, 20)

    # split_video_into_separate_measures("A Town with an Ocean View (Kiki's Delivery Service) - Guitar.mp4", sky_guitar_settings, 18)
    # combine_measures_into_pages(sky_guitar_settings)
    # split_video_into_separate_measures("SPRING DAY, CHERRY BLOSSOMS.mp4", piano_settings, 4, False)
    # combine_measures_into_pages(piano_settings)
    # split_video_into_separate_measures("videos/Reflections.mp4", sky_guitar_settings_fhd_tabs_up, 12, True)
    # split_video_into_separate_measures("videos/La_Lagrima.mp4", sky_guitar_settings_fhd_tabs_down, 10, True)
    # split_video_into_separate_measures("Libertango - A. Piazzolla.mp4", smile_guitar_settings, 12, False)
    # MeasuresService.split_video_into_separate_measures("videos/Always_with_me.mp4", kenneth_guitar_settings, 4, False, False)
    TrimService.trim_all_measures(kenneth_guitar_settings)
    # PagesService.combine_measures_into_pages(kenneth_guitar_settings, 'trimmed')


run()
