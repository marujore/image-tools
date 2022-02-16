import os
from collections.abc import Iterable

import rasterio
from colorama import Fore
from colorama import Style


def describe_img(img_path, print_info=False):
    """
    Prints the metadata of an image
    :param img_path: path to image
    :param print_info: print condition
    :return: None
    """
    with rasterio.open(img_path) as src:
        if print_info:
            for k, v in src.profile.items():
                print(f"{k}: {v}")
        return src.profile


def img_description_are_equal(img1_path, img2_path, print_info=True):
    """
    Compares the metadata of two images
    :param img1_path: path to image 1
    :param img2_path: path to image 2
    :param print_info: print condition
    :return: True if equal, False if not
    """
    img1_desc = describe_img(img1_path, print_info=False)
    img2_desc = describe_img(img2_path, print_info=False)
    if img1_desc == img2_desc:
        if print_info:
            print(f"{Fore.GREEN}Equal{Style.RESET_ALL}: \n{img1_path} \n{img2_path}", flush=True)
            print()
        return True
    else:
        print(f"{Fore.RED}Different{Style.RESET_ALL}: \n{img1_path} \n{img2_path}", flush=True)
        if print_info:
            for key in img1_desc:
                equal = img1_desc[key] == img2_desc[key]
                if equal:
                    print(f"{Fore.GREEN}{key}{Style.RESET_ALL}: {img1_desc[key]}")
                else:
                    if not isinstance(img1_desc[key], str) and isinstance(img1_desc[key], Iterable):
                        print(f"{Fore.RED}{key}{Style.RESET_ALL}:", flush=True)
                        for a, b in zip(img1_desc[key], img2_desc[key]):
                            equal = a == b
                            if equal:
                                print(f"{a} {b}", flush=True)
                            else:
                                print(f"{Fore.RED}{a} {b}{Style.RESET_ALL}", flush=True)
                    else:
                        print(f"{Fore.RED}{key}{Style.RESET_ALL}: {img1_desc[key]} {img2_desc[key]}", flush=True)
            print()
        return False


def folder_img_description_are_equal(img_folder, extension='tif', print_info=False):
    """
    Compares the metadata of two images
    :param img_folder: path folder containing images
    :param extension: file extension format
    :param print_info: print condition
    :return: True if equal, False if not
    """
    img_list = []
    for file in os.listdir(img_folder):
        if file.endswith(extension):
            img_list.append(os.path.join(img_folder, file))
    for img in img_list[1:]:
        img_description_are_equal(img_list[0], img, print_info=True)
    return
