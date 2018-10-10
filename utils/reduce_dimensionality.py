import argparse
from os import listdir
from os.path import isfile, join

import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import logging
from scipy.io import loadmat, savemat

from datapaths import DATASET_PATH, HYPER_BANDS_FILE, HYPER_FOLDER_PATH

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(lineno)d:%(message)s')
log = logging.getLogger(__file__)


def trim_bands(source_list, filter_list):
    trimmed = []
    for i in range(len(filter_list)):
        if filter_list[i] == 0:
            trimmed.append(source_list[i])
    return trimmed


def purge_noisy_bands(image, band_filter):
    # 369 usable bands per pixel
    out = np.zeros([80, 80, 369])
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            out[i][j] = trim_bands(image[i][j], band_filter)
    return out


def get_configured_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--merge-bands', default=False, dest='merge_bands',
                        help='Merge bands with averaging for bands with low symmetric KL Divergence')
    return parser


def fetch_file_names():
    try:
        hyper_files = sorted([hyper_file for hyper_file in
                              [f for f in listdir(HYPER_FOLDER_PATH) if isfile(join(HYPER_FOLDER_PATH, f))]])
        hyper_bands = pd.read_csv(HYPER_BANDS_FILE)
    except FileNotFoundError:
        print(DATASET_PATH)
        print("Failed to find Processed Dataset.\nPlease follow the README instructions to fetch and process the dataset")
    return hyper_files, hyper_bands


def clean_hyper_images():
    for hyper_file in hyper_files[3:4]:
        clean_image = purge_noisy_bands(
            loadmat(HYPER_FOLDER_PATH + hyper_file)['image'], hyper_bands['Noise_flag'])
        savemat(HYPER_FOLDER_PATH + hyper_file, {'image': clean_image})


if __name__ == '__main__':
    log.info('Starting Execution')
    parser = get_configured_parser()

    args = parser.parse_args()
    args.merge_bands = bool(args.merge_bands)

    hyper_files, hyper_bands = fetch_file_names()
    log.info('Fetched all the Hyperspectral File Names')
    clean_hyper_images()
    log.info('Clean off all the noisy bands')
    if args.merge_bands:
        # TODO Add Band Merging using KL Divergence here
        pass
    log.info('Execution Completed')
