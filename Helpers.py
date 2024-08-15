import os
from natsort import natsorted, ns


def get_images_paths(dir_name: str) -> list[str]:
    final_list_of_paths = []
    for root, dirs, files in os.walk(dir_name):
        sorted_files = natsorted(files, alg=ns.IGNORECASE)
        for filename in sorted_files:
            final_list_of_paths.append(os.path.join(root, filename))
    return final_list_of_paths
