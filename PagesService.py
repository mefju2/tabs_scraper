import cv2
import numpy as np
from Page import Page
from Helpers import get_images_paths


def combine_measures_into_pages(settings, dir_name):
    measure_height = settings.crop_height_cords[1] - settings.crop_height_cords[0]
    page_height = measure_height * settings.amount_of_rows
    current_page_height = measure_height
    page_width = 0

    current_page = Page(1, settings)

    for measure_path in get_images_paths(dir_name):
        if current_page.saved_on_disk:
            current_page = Page(current_page.index + 1, settings)

        measure_img = cv2.imread(measure_path)

        if len(measure_img[1]) < settings.video_width:
            padding_width = settings.video_width - measure_img.shape[1]
            padding = np.full((measure_img.shape[0], padding_width, 3), fill_value=242, dtype=np.uint8)

            # Concatenate the smaller array with the padding
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
