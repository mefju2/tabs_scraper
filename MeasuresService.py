import cv2

from settings import Settings
import Helpers


def get_measures_section(frame, settings: Settings, test_measurement_section: bool):
    section = frame[
                  settings.measure_number_height_cords[0]:settings.measure_number_height_cords[1],
                  settings.measure_number_width_cords[0]:settings.measure_number_width_cords[1]
              ]

    if test_measurement_section:
        frame[
            settings.measure_number_height_cords[0]:settings.measure_number_height_cords[1],
            settings.measure_number_width_cords[0]:settings.measure_number_width_cords[1]
        ] = [0, 0, 255]
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
    c_ocr = Helpers.read_measure_with_ocr(current_measure)
    p_ocr = Helpers.read_measure_with_ocr(previous_measure)
    # if 80 > count > 20:
    # cv2.imwrite(f"debug/{count}_{different}_{c_ocr}_current_measure.jpg", current_measure)
    # cv2.imwrite(f"debug/{count}_{different}_{p_ocr}_previous_measure.jpg", previous_measure)
    if c_ocr == p_ocr:
        print(count, c_ocr, p_ocr, 'equal')
        return True
    print(count, c_ocr, p_ocr)
    return False
    # return True


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

            if not test_measurement_section and measures_are_equal(current_measure, previous_measure, "measures",
                                                                   count):
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
