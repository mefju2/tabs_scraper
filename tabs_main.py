import cv2
import numpy as np
import pytesseract
from settings import Settings


def extractImagesHorizontal(pathIn, pathOut):
    count = 14
    vidcap = cv2.VideoCapture(pathIn)
    success, image = vidcap.read()
    success = True
    blank_image = np.zeros((1920, 1280, 3), np.uint8)
    page_height = 320
    current_page = [None, None, None, None, None, None]
    page_part_counter = 0

    while success:
        vidcap.set(cv2.CAP_PROP_POS_MSEC,(count*950))
        success,image = vidcap.read()
        print('Read a new frame: ', success)

        if image is not None:
            cropped_img = image[400:1080, 0:1920]

            a4 = blank_image
            a4[page_height - 320:page_height, 0:1280] = cropped_img

            #cv2.imwrite(f"{pathOut}/frame_{count}.jpg", cropped_img)
            current_page[page_part_counter] = a4

            if page_height == 1920:
                cv2.imwrite(f"{pathOut}/a4_full_{count}.jpg", a4)
                page_height = 320
                blank_image[:, :] = (255, 255, 255)
                page_part_counter = 0
                current_page = [None, None, None, None, None, None]
            else:
                #cv2.imwrite(f"{pathOut}/a4_{count}.jpg", a4)
                page_height += 320

            count = count + 14
    cv2.imwrite(f"{pathOut}/a4_full_{count}.jpg", current_page[page_part_counter])


def extract_images_vertical(path_in, path_out, increment_by, settings):
    vidcap = cv2.VideoCapture(path_in)
    success, image = vidcap.read()
    success = True

    page_height = settings.crop_height_cords[1] - settings.crop_height_cords[0]
    current_page_height = page_height
    page_width = 0

    blank_image = np.zeros((page_height * 5, 2560, 3), np.uint8)  # 320 * 5 / 1280 * 2
    blank_image[:, :] = (255, 255, 255)

    current_page = [None, None, None, None, None]
    page_part_counter = 0
    previous_measure_number = 5
    previous_measure = None
    count = increment_by

    while success:
        vidcap.set(cv2.CAP_PROP_POS_MSEC,(count*950))
        success, image = vidcap.read()
        # print('Read a new frame: ', success)

        if image is not None:  # image is 720x1280
            cropped_img = image[
                          settings.crop_height_cords[0]: settings.crop_height_cords[1],
                          0:1280]

            current_measure = get_measures_section(image, settings)
            # measure_number = get_measure_number(image, previous_measure_number, pathOut, settings)
            # if measure_number == 56:
            #     cv2.imwrite(f"{pathOut}/measure_{measure_number}_{count}.jpg", cropped_img)
            # print(measure_number)

            # difference_between_measures = abs(measure_number - previous_measure_number)
            # print(f"|{measure_number} - {previous_measure_number}| = {difference_between_measures}")
            # if measure_number != previous_measure_number and 3 < difference_between_measures < 7:
            if previous_measure is None or not measures_are_equal(current_measure, previous_measure, path_out, count):
                # print(count)
                a4 = blank_image
                a4[current_page_height - page_height:current_page_height, page_width:page_width + 1280] = cropped_img

                # cv2.imwrite(f"{path_out}/frame_{count}.jpg", cropped_img)
                current_page[page_part_counter] = a4

                if page_width == 1280:
                    page_width = 0

                    if current_page_height == page_height * 5:
                        print(count, '!!!')
                        cv2.imwrite(f"{path_out}/a4_full_{count}.jpg", a4)
                        current_page_height = page_height
                        blank_image[:, :] = (255, 255, 255)
                        page_part_counter = 0
                        current_page = [None, None, None, None, None]
                    else:
                        # cv2.imwrite(f"{path_out}/a4_{count}.jpg", a4)
                        current_page_height += page_height
                        # page_part_counter += 1
                else:
                    page_width += 1280

            count = count + increment_by
            previous_measure = current_measure
    if current_page[0] is not None:  # po to zapisać kartkę, gdy ta nie jest zapełniona do końca
        cv2.imwrite(f"{path_out}/a4_full_{count}.jpg", current_page[page_part_counter])


def get_measures_section(frame, settings):
    return frame[
                  settings.measure_number_height_cords[0]:settings.measure_number_height_cords[1],
                  settings.measure_number_width_cords[0]:settings.measure_number_width_cords[1]
                  ]


def measures_are_equal(current_measure, previous_measure, path_out, count):
    different = 0

    for i in range(len(current_measure)):
        for j in range(len(current_measure[0])):
            f = current_measure[i][j]
            pf = previous_measure[i][j]
            if (f - pf).any():
                different += 1

    # print(f'{str(len(current_measure) * len(current_measure[0] * 3))} - {different}')

    if different > 200:
        c_ocr = read_measure_with_ocr(current_measure, count)
        p_ocr = read_measure_with_ocr(previous_measure, count)
        # if 100 > count > 50:
        #     cv2.imwrite(f"{path_out}/{count}_{different}_{c_ocr}_current_measure.jpg", current_measure)
        #     cv2.imwrite(f"{path_out}/{count}_{different}_{p_ocr}_previous_measure.jpg", previous_measure)
        if c_ocr == p_ocr:
            print(count, 'ocr equal: ', c_ocr, p_ocr)
            return True
        print(count, c_ocr, p_ocr)
        return False
    return True


def read_measure_with_ocr(measure, count):
    read_number = pytesseract.image_to_string(measure, config='--psm 6').strip()

    # obsługa wyjątków gdy ocr źle przeczyta
    if read_number == 'oL':
        return '51'
    if '.' in read_number:
        read_number = read_number.replace('.', '')

    return read_number.lower()


def run():
    guitar_settings = Settings((400, 720), (430, 460), (45, 80))
    piano_settings = Settings((0, 255), (0, 25), (110, 150))
    out_path = "frames"
    # extractImagesHorizontal(in_path, out_path)
    # extractImagesVertical("The Entertainer.mp4", out_path, 14)  # The Entertainer
    extract_images_vertical("Married_Life.mp4", out_path, 10, guitar_settings)  # Married Life
    #extract_images_vertical("SPRING DAY, CHERRY BLOSSOMS.mp4", out_path, 4, piano_settings)  # Married Life


run()
