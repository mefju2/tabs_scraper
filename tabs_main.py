import cv2
import numpy as np
import pytesseract
import os
from natsort import natsorted, ns

from Page import Page
from settings import Settings


def get_measures_section(frame, settings, test_measurement_section: bool):
    section = frame[
              settings.measure_number_height_cords[0]:settings.measure_number_height_cords[1],
              settings.measure_number_width_cords[0]:settings.measure_number_width_cords[1]]

    if test_measurement_section:
        frame[
            settings.measure_number_height_cords[0]:settings.measure_number_height_cords[1],
            settings.measure_number_width_cords[0]:settings.measure_number_width_cords[1]] = [0, 0, 255]
        cv2.imwrite(f"debug/test_current_measure.jpg", frame)

    return section


def measures_are_equal(current_measure, previous_measure, path_out, count):
    if previous_measure is None:
        return False

    # different = 0
    #
    # for i in range(len(current_measure)):
    #     for j in range(len(current_measure[0])):
    #         f = current_measure[i][j]
    #         pf = previous_measure[i][j]
    #         if (f - pf).any():
    #             different += 1
    #
    #     if different > 200:
    c_ocr = read_measure_with_ocr(current_measure)
    p_ocr = read_measure_with_ocr(previous_measure)
    # if 80 > count > 20:
    # cv2.imwrite(f"debug/{count}_{different}_{c_ocr}_current_measure.jpg", current_measure)
    # cv2.imwrite(f"debug/{count}_{different}_{p_ocr}_previous_measure.jpg", previous_measure)
    if c_ocr == p_ocr:
        print(count, c_ocr, p_ocr, 'equal')
        return True
    print(count, c_ocr, p_ocr)
    return False
    # return True


def read_measure_with_ocr(measure):
    read_number = pytesseract.image_to_string(measure, config='--psm 6').strip()

    # handling weird ocr reads
    if read_number == 'oL':
        return '51'
    if '.' in read_number:
        read_number = read_number.replace('.', '')

    return read_number.lower()


def split_video_into_separate_measures(
        video_name: str,
        settings: Settings,
        increment_by: int,
        compare_to_previous_measure: bool,
        test_measurement_section: bool = False,
        skip_before: int = 0,
        stop_at: int = 0
):
    vidcap = cv2.VideoCapture(video_name)
    vidcap.read()
    success = True
    count = 0
    previous_measure = None
    current_measure = None

    while success:
        count = count + increment_by

        if skip_before > 0:
            if count < skip_before:
                continue
        if stop_at > 0:
            if count > stop_at:
                return

        vidcap.set(cv2.CAP_PROP_POS_MSEC, (count * 950))
        success, image = vidcap.read()

        if image is None:
            continue

        if compare_to_previous_measure:
            current_measure = get_measures_section(image, settings, test_measurement_section)

            if not test_measurement_section and measures_are_equal(current_measure, previous_measure, "measures", count):
                continue

        cropped_img = image[
                      settings.crop_height_cords[0]: settings.crop_height_cords[1],
                      0:settings.video_width]
        # cv2.imshow('test', cropped_img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        cv2.imwrite(f"measures/{count}.jpg", cropped_img)

        if compare_to_previous_measure:
            previous_measure = current_measure


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

    current_page = Page(1, settings)

    for measure_path in get_measures_paths():
        if current_page.saved_on_disk:
            current_page = Page(current_page.index + 1, settings)

        measure_img = cv2.imread(measure_path)

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


def run():
    os.makedirs("pages", exist_ok=True)
    os.makedirs("measures", exist_ok=True)

    # sky_guitar_settings = Settings((400, 720), (430, 460), (45, 80), 6)
    sky_guitar_settings = Settings((400, 720), (450, 480), (45, 78), 5, 1280, 720)
    sky_guitar_settings_fhd_tabs_up = Settings((0, 500), (56, 88), (80, 110), 5, 1920, 1080)
    sky_guitar_settings_fhd_tabs_down = Settings((600, 1080), (658, 688), (88, 122), 5, 1920, 1080)
    smile_guitar_settings = Settings((645, 1080), (650, 685), (0, 25), 6, 1920, 1080)
    sky_guitar_settings_small = Settings((0, 168), (24, 40), (26, 42), 5, 640, 360)
    # kenneth_guitar_settings = Settings((480, 720), (585, 635), (180, 230), 5)
    piano_settings = Settings((0, 255), (0, 25), (110, 150), 5, 1280, 720)
    out_path = "frames"
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

    combine_measures_into_pages(sky_guitar_settings_fhd_tabs_down)


run()
