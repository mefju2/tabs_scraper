import os
import pytesseract
from natsort import natsorted, ns


def get_images_paths(dir_name: str) -> list[str]:
    final_list_of_paths = []
    for root, dirs, files in os.walk(dir_name):
        sorted_files = natsorted(files, alg=ns.IGNORECASE)
        for filename in sorted_files:
            final_list_of_paths.append(os.path.join(root, filename))
    return final_list_of_paths


def read_measure_with_ocr(measure):
    read_number = pytesseract.image_to_string(measure, config='--psm 6').strip()

    # handling weird ocr reads
    if read_number == '3}':
        return 5
    if read_number == 'il':
        return 11
    if read_number == 'oL':
        return '51'
    if '.' in read_number:
        read_number = read_number.replace('.', '')

    read_number = read_number.replace(')', '').replace(':', '')

    return read_number.lower()
