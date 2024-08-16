import cv2
import numpy as np

import Helpers
from Helpers import get_images_paths


def trim_all_measures(settings):
    previous_measure_number = ''
    measure_paths = get_images_paths('measures')
    last_measure = measure_paths[-1]
    all_trimmed_measures = []

    for measure_path in measure_paths:
        list_of_measures = []
        frame_number = measure_path.replace('measures/', '').replace('.jpg', '')

        measure_img = cv2.imread(measure_path)
        print(measure_path)

        is_last_measure = measure_path == last_measure
        if is_last_measure:
            measure_img[105:235, -1] = [0, 0, 0]
            cv2.imwrite(f"debug/last_measure.jpg", measure_img)

        previous_measure_number = trim_single_measure(settings, measure_img, list_of_measures, all_trimmed_measures, previous_measure_number, is_last_measure)

        # for i, measure in enumerate(list_of_measures):
        #     cv2.imwrite(f"trimmed/{frame_number}_{i}.jpg", measure)

        combined = np.concatenate(list_of_measures, axis=1)
        cv2.imwrite(f"trimmed/{frame_number}_trimmed.jpg", combined)

    return all_trimmed_measures


def trim_single_measure(settings, image, list_of_measures, all_trimmed_measures, previous_measure_number, is_last_measure):
    is_first_line_found = False
    measure_first_pixel = 0
    current_measure_number_ocr = ''

    for i in range(settings.video_width):
        is_last_pixel_in_last_measure = is_last_measure and i == settings.video_width - 1
        if not is_last_pixel_in_last_measure and not is_measure_separating_line(image, i):
            continue

        # print(sum_of_black)
        # image[105:235, i] = [0, 0, 255]  # debug red coloring

        if not is_first_line_found:
            measure_first_pixel = i
            is_first_line_found = True
            continue

        measure_length_in_pixels = i - measure_first_pixel
        if is_last_measure or measure_length_in_pixels > 200:
            current_measure_number_ocr = get_measure_number(image, i)
            # print(f'{frame_number}_{measure_length_in_pixels}')
            if previous_measure_number != current_measure_number_ocr:
                trimmed_measure = image[
                        0:settings.crop_height_cords[1] - settings.crop_height_cords[0],
                        measure_first_pixel:i
                    ]
                list_of_measures.append(trimmed_measure)
                all_trimmed_measures.append(trimmed_measure)

            measure_first_pixel = i
    return current_measure_number_ocr


def get_measure_number(image, pixel_index):
    measure_number_image = image[75:103, pixel_index-18:pixel_index+18]
    measure_number_ocr = Helpers.read_measure_with_ocr(measure_number_image)
    print(measure_number_ocr)
    # image[75:103, pixel_index-18:pixel_index+18] = [255, 0, 0]
    return measure_number_ocr


def is_measure_separating_line(image, pixel_index):
    if np.sum(image[170, pixel_index]) > 150:  # check if pixel is black enough
        return False

    sum_of_pixels_in_vertical_line = np.sum(image[105:235, pixel_index])
    if sum_of_pixels_in_vertical_line > 14_000:  # check if other pixels in straight vertical line are also black
        return False

    # image[965:980, i - 7:i + 7] = [0, 0, 255]
    sum_of_pixels_around_single_point = np.sum(image[165:180, pixel_index - 7:pixel_index + 7])
    if sum_of_pixels_around_single_point < 100_000:  # to separate measure lines from curly lines
        return False

    return True
