import cv2
import numpy as np
from Page import Page
from Helpers import get_images_paths
from settings import Settings


def combine_measures_into_pages(settings, source_dir_name: str):
    measure_height = settings.crop_height_cords[1] - settings.crop_height_cords[0]
    current_page_height = measure_height
    page_width = 0
    current_page = Page(1, settings)

    for measure_path in get_images_paths(source_dir_name):
        if current_page.saved_on_disk:
            current_page = Page(current_page.index + 1, settings)

        measure_img = cv2.imread(measure_path)

        if len(measure_img[1]) < settings.video_width:
            padding_width = settings.video_width - measure_img.shape[1]
            padding = np.full((measure_img.shape[0], padding_width, 3), fill_value=242, dtype=np.uint8)
            measure_img = np.concatenate((measure_img, padding), axis=1)

        current_page.content[
            current_page_height - measure_height:current_page_height,
            page_width:page_width + settings.video_width
        ] = measure_img

        if page_width == settings.video_width:
            page_width = 0

            if current_page_height == measure_height * settings.amount_of_rows:
                cv2.imwrite(f"pages/a4_full_{current_page.index}.jpg", current_page.content)
                current_page_height = measure_height
                current_page.saved_on_disk = True
            else:
                current_page_height += measure_height
        else:
            page_width += settings.video_width

    if not current_page.saved_on_disk:  # printing the last page if it's not filled up
        cv2.imwrite(f"pages/a4_full_{current_page.index}.jpg", current_page.content)


def combine_trimmed_measures_into_pages(settings: Settings, list_of_trimmed_measures):
    current_page = Page(1, settings)
    measure_height = settings.crop_height_cords[1] - settings.crop_height_cords[0]
    current_page_height = measure_height

    for trimmed_measure in list_of_trimmed_measures:
        if current_page.saved_on_disk:
            current_page = Page(current_page.index + 1, settings)

        current_page.content[
            current_page_height - measure_height:current_page_height,
            0:settings.video_width * 2
        ] = trimmed_measure

        if current_page_height == measure_height * settings.amount_of_rows:
            cv2.imwrite(f"pages/a4_full_{current_page.index}.jpg", current_page.content)
            current_page_height = measure_height
            current_page.saved_on_disk = True
        else:
            current_page_height += measure_height

    if not current_page.saved_on_disk:  # printing the last page if it's not filled up
        cv2.imwrite(f"pages/a4_full_{current_page.index}.jpg", current_page.content)


def organize_trimmed_measures(settings: Settings, list_of_measures: list):
    organized_list = []
    measure = []
    print_page_width = settings.video_width * 2

    for measure_piece in list_of_measures:
        if len(measure) == 0:
            measure.append(measure_piece)
            continue

        potential_measure_length = len(measure[-1][1]) + len(measure_piece[1])
        if potential_measure_length > print_page_width:
            fill_blanks_and_add_to_main_list(print_page_width, measure, organized_list)
            measure = [measure_piece]
            continue

        measure[-1] = np.concatenate((measure[-1], measure_piece), axis=1)

    fill_blanks_and_add_to_main_list(print_page_width, measure, organized_list)
    return organized_list


def fill_blanks_and_add_to_main_list(print_page_width, measure, organized_list):
    padding_width = print_page_width - len(measure[-1][1])
    padding = np.full((measure[-1].shape[0], padding_width, 3), fill_value=242, dtype=np.uint8)
    measure_with_filled_blanks = np.concatenate((measure[-1], padding), axis=1)

    organized_list.append(measure_with_filled_blanks)

