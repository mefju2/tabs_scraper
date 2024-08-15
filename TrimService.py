import cv2
import numpy as np

from Helpers import get_images_paths


def trim_all_measures(settings):
    for measure_path in get_images_paths('measures'):
        list_of_measures = []
        frame_number = measure_path.replace('measures/', '').replace('.jpg', '')

        measure_img = cv2.imread(measure_path)
        print(measure_path)

        trim_single_measure(settings, measure_img, list_of_measures, frame_number)

        # for i, measure in enumerate(list_of_measures):
        #     cv2.imwrite(f"trimmed/{frame_number}_{i}.jpg", measure)

        combined = np.concatenate(list_of_measures, axis=1)
        cv2.imwrite(f"trimmed/{frame_number}_trimmed.jpg", combined)


def trim_single_measure(settings, image, list_of_measures, frame_number):
    is_first_line_found = False
    measure_first_pixel = 0

    for i in range(settings.video_width):
        if not is_measure_separating_line(image, i):
            continue

        # print(sum_of_black)
        image[105:235, i] = [0, 0, 255]  # debug red coloring

        if not is_first_line_found:
            measure_first_pixel = i
            is_first_line_found = True
            continue

        measure_length_in_pixels = i - measure_first_pixel
        if measure_length_in_pixels > 200:
            print(f'{frame_number}_{measure_length_in_pixels}')
            list_of_measures.append(
                image[
                    0:settings.crop_height_cords[1] - settings.crop_height_cords[0],
                    measure_first_pixel:i
                ]
            )
            measure_first_pixel = i


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
