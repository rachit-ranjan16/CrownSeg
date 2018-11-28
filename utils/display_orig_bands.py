from os import listdir
from os.path import isfile, join
from scipy.io import loadmat
from configparser import ConfigParser

import argparse
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from datapaths import DATASET_PATH, HYPER_BANDS_FILE, HYPER_ORIG_FOLDER_PATH, CONFIG_FILE


def plot_bands(wavelengths, intensities):
    plt.style.use('ggplot')
    f, ax = plt.subplots(1, 1)
    ax.set_xlabel('Band Nanometers')
    ax.set_ylabel('Intensity')
    ax.plot(wavelengths, intensities)
    plt.show()


def get_configured_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--image-id', default=3, dest='img_id',
                        choices=[str(x) for x in range(1, 52)])
    parser.add_argument('-x', default=40, dest='x',
                        help='X coordinate less than 80')
    parser.add_argument('-y', default=25, dest='y',
                        help='Y coordinate less than 80')
    return parser


def get_parsed_args():
    args = parser.parse_args()
    args.x = int(args.x)
    args.y = int(args.y)
    args.img_id = int(args.img_id)
    return args


if __name__ == '__main__':
    parser = get_configured_parser()
    args = get_parsed_args()
    config = ConfigParser()
    config.read(CONFIG_FILE)

    try:
        hyper_files = sorted([hyper_file for hyper_file in
                              [f for f in listdir(HYPER_ORIG_FOLDER_PATH) if isfile(join(HYPER_ORIG_FOLDER_PATH, f))]])
        hyper_bands = pd.read_csv(HYPER_BANDS_FILE)
    except FileNotFoundError:
        print(DATASET_PATH)
        print("Failed to find Processed Dataset.\nPlease follow the README instructions to fetch and process the dataset")
    hyper_image = loadmat(HYPER_ORIG_FOLDER_PATH +
                              hyper_files[args.img_id])['image']
    wavelengths = hyper_bands['Band_nanometers']
    plot_bands(wavelengths=wavelengths, intensities=hyper_image[args.x][args.y])
