import cv2
import numpy as np
import pytesseract


def extractImagesHorizontal(pathIn, pathOut):
    count = 14
    vidcap = cv2.VideoCapture(pathIn)
    success,image = vidcap.read()
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


def extractImagesVertical(pathIn, pathOut, increment_by):
    count = increment_by
    vidcap = cv2.VideoCapture(pathIn)
    success,image = vidcap.read()
    success = True
    blank_image = np.zeros((1600, 2560, 3), np.uint8)  # 320 * 5 / 1280 * 2
    blank_image[:, :] = (255, 255, 255)
    page_height = 320
    page_width = 0
    current_page = [None, None, None, None, None]
    page_part_counter = 0
    previous_measure_number = 5

    while success:
        vidcap.set(cv2.CAP_PROP_POS_MSEC,(count*950))
        success, image = vidcap.read()
        # print('Read a new frame: ', success)

        if image is not None:
            cropped_img = image[400:1080, 0:1920]

            a4 = blank_image
            a4[page_height - 320:page_height, page_width:page_width + 1280] = cropped_img

            measure_number = get_measure_number(image, previous_measure_number, pathOut)
            # if measure_number == 56:
            #     cv2.imwrite(f"{pathOut}/measure_{measure_number}_{count}.jpg", cropped_img)
            # print(measure_number)

            difference_between_measures = abs(measure_number - previous_measure_number)
            print(f"|{measure_number} - {previous_measure_number}| = {difference_between_measures}")
            if measure_number != previous_measure_number and 3 < difference_between_measures < 7:
                print("passed")
                previous_measure_number = measure_number

                # cv2.imwrite(f"{pathOut}/frame_{count}.jpg", cropped_img)
                current_page[page_part_counter] = a4

                if page_width == 1280:
                    page_width = 0

                    if page_height == 1600:
                        cv2.imwrite(f"{pathOut}/a4_full_{count}.jpg", a4)
                        page_height = 320
                        blank_image[:, :] = (255, 255, 255)
                        page_part_counter = 0
                        current_page = [None, None, None, None, None]
                    else:
                        # cv2.imwrite(f"{pathOut}/a4_{count}.jpg", a4)
                        page_height += 320
                else:
                    page_width += 1280

            count = count + increment_by
    if current_page[0] is not None:
        cv2.imwrite(f"{pathOut}/a4_full_{count}.jpg", current_page[page_part_counter])


def get_measure_number(image, previous_measure_number, pathOut):
    measure_img = image[430:460, 45:80]
    measure_number = pytesseract.image_to_string(measure_img, config='--psm 6').strip()
    if 'l' in measure_number:
        measure_number = measure_number.replace('l', '1')
    elif '1' in measure_number and 's' in measure_number.lower():
        return 115

    if measure_number == "":
        return 1
    else:
        try:
            return int(measure_number)
        except ValueError:
            print(f"Invalid OCR read: {measure_number}")
            cv2.imwrite(f"{pathOut}/invalid_ocr_red_{measure_number}.jpg", measure_img)
            return previous_measure_number


def run():
    out_path = "frames"
    # extractImagesHorizontal(in_path, out_path)
    # extractImagesVertical("The Entertainer.mp4", out_path, 14)  # The Entertainer
    extractImagesVertical("Married_Life.mp4", out_path, 7)  # Married Life


run()
