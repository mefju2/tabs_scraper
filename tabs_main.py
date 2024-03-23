import cv2
import numpy as np
import pytesseract
import os
from natsort import natsorted, ns

from Page import Page
from settings import Settings


def get_measures_section(frame, settings):
    return frame[
           settings.measure_number_height_cords[0]:settings.measure_number_height_cords[1],
           settings.measure_number_width_cords[0]:settings.measure_number_width_cords[1]]


def measures_are_equal(current_measure, previous_measure, path_out, count):
    if previous_measure is None:
        return False

    different = 0

    for i in range(len(current_measure)):
        for j in range(len(current_measure[0])):
            f = current_measure[i][j]
            pf = previous_measure[i][j]
            if (f - pf).any():
                different += 1

    if different > 200:
        c_ocr = read_measure_with_ocr(current_measure)
        p_ocr = read_measure_with_ocr(previous_measure)
        # if 80 > count > 20:
        #     cv2.imwrite(f"{path_out}/{count}_{different}_{c_ocr}_current_measure.jpg", current_measure)
        #     cv2.imwrite(f"{path_out}/{count}_{different}_{p_ocr}_previous_measure.jpg", previous_measure)
        if c_ocr == p_ocr:
            print(count, c_ocr, p_ocr, 'equal')
            return True
        print(count, c_ocr, p_ocr)
        return False
    return True


def read_measure_with_ocr(measure):
    read_number = pytesseract.image_to_string(measure, config='--psm 6').strip()

    # handling weird ocr reads
    if read_number == 'oL':
        return '51'
    if '.' in read_number:
        read_number = read_number.replace('.', '')

    return read_number.lower()


def split_video_into_separate_measures(video_name, settings, increment_by):
    vidcap = cv2.VideoCapture(video_name)
    vidcap.read()
    success = True
    count = increment_by
    previous_measure = None

    while success:
        # if count > 40:
        #     return

        vidcap.set(cv2.CAP_PROP_POS_MSEC, (count * 950))
        success, image = vidcap.read()

        while success:
            if image is None:
                continue

            current_measure = get_measures_section(image, settings)

            if measures_are_equal(current_measure, previous_measure, "measures", count):
                continue

            cropped_img = image[
                          settings.crop_height_cords[0]: settings.crop_height_cords[1],
                          0:1280]
            cv2.imwrite(f"measures/{count}.jpg", cropped_img)
            previous_measure = current_measure
            count = count + increment_by


def get_measures_paths():
    final_list_of_paths = []
    for root, dirs, files in os.walk('measures'):
        sorted_files = natsorted(files, alg=ns.IGNORECASE)
        for filename in sorted_files:
            final_list_of_paths.append(os.path.join(root, filename))
    return final_list_of_paths


def combine_measures_into_pages(settings):
    measure_height = settings.crop_height_cords[1] - settings.crop_height_cords[0]
    page_height = measure_height * settings.amount_of_rows
    current_page_height = measure_height
    page_width = 0

    current_page = Page(1, page_height)

    for measure_path in get_measures_paths():
        if current_page.saved_on_disk:
            current_page = Page(current_page.index + 1, page_height)

        measure_img = cv2.imread(measure_path)

        current_page.content[
            current_page_height - measure_height:current_page_height,
            page_width:page_width + 1280
        ] = measure_img

        if page_width == 1280:
            page_width = 0

            if current_page_height == measure_height * settings.amount_of_rows:
                cv2.imwrite(f"pages/a4_full_{current_page.index}.jpg", current_page.content)
                current_page_height = measure_height
                current_page.saved_on_disk = True
            else:
                current_page_height += measure_height
        else:
            page_width += 1280

    if not current_page.saved_on_disk:  # printing the last page if it's not filled up
        cv2.imwrite(f"pages/a4_full_{current_page.index}.jpg", current_page.content)


def run():
    os.makedirs("pages", exist_ok=True)
    os.makedirs("measures", exist_ok=True)

    sky_guitar_settings = Settings((400, 720), (430, 460), (45, 80), 6)
    kenneth_guitar_settings = Settings((480, 720), (585, 635), (180, 230), 5)
    piano_settings = Settings((0, 255), (0, 25), (110, 150), 5)
    out_path = "frames"
    # extractImagesVertical("The Entertainer.mp4", out_path, 14)
    # extract_images_vertical("Married_Life.mp4", out_path, 10, sky_guitar_settings, (230,))
    # extract_images_vertical("SPRING DAY, CHERRY BLOSSOMS.mp4", out_path, 4, piano_settings)
    # extract_images_vertical("KISS THE RAIN.mp4", out_path, 8, Settings((0, 220), (0, 32), (78, 110), 6), (64, 160))
    # extract_images_vertical("Interstellar.mp4", out_path, 8, Settings((0, 220), (0, 32), (78, 110), 6), (64, 160))
    # extract_images_vertical("ALWAYS WITH ME.mp4", out_path, 3, Settings((0, 220), (0, 32), (78, 110), 6), (64, 160))
    # extract_images_vertical("Interstellar_guitar.mp4", out_path, 7, kenneth_guitar_settings)
    # extract_images_vertical("Kiss the Rain - Guitar Lesson.mp4", out_path, 8, sky_guitar_settings)

    # split_video_into_separate_measures("Kiss the Rain - Guitar Lesson.mp4", sky_guitar_settings, 20)
    combine_measures_into_pages(sky_guitar_settings)


run()
