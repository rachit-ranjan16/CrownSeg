import argparse
from os import listdir
from os.path import isfile, join

import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.io import loadmat

from datapaths import DATASET_PATH, HYPER_BANDS_FILE, HYPER_FOLDER_PATH


def plot_bands(wavelengths, intensities):
    plt.style.use('ggplot')
    f, ax = plt.subplots(1, 1)
    ax.set_xlabel('Wavelength(nm)')
    ax.set_ylabel('Intensity')
    ax.plot(wavelengths, intensities)
    plt.show()


def trim_bands(source_list, flags):
    trimmed = []
    for i in range(len(flags)):
        if flags[i] == 0:
            trimmed.append(source_list[i])
    return trimmed


def get_configured_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--image-id', default=3, dest='img_id',
                        choices=[str(x) for x in range(1, 52)])
    parser.add_argument('-x', default=40, dest='x',
                        help='X coordinate less than 80')
    parser.add_argument('-y', default=25, dest='y',
                        help='Y coordinate less than 80')
    parser.add_argument('--trim-image', default=False, dest='trim_image',
                        help='Set to True if noisy bands need to be removed both from wavelengths and hyperspectral images')
    parser.add_argument('--trim-wavelengths', default=True, dest='trim_w',
                        help='Set to True if noisy bands need to be removed from wavelengths alone')
    return parser


if __name__ == '__main__':
    parser = get_configured_parser()
    args = parser.parse_args()
    args.x = int(args.x)
    args.y = int(args.y)
    args.trim_image = bool(args.trim_image)
    args.trim_w = bool(args.trim_w)
    args.img_id = int(args.img_id)

    try:
        hyper_files = sorted([hyper_file for hyper_file in
                              [f for f in listdir(HYPER_FOLDER_PATH) if isfile(join(HYPER_FOLDER_PATH, f))]])
        hyper_bands = pd.read_csv(HYPER_BANDS_FILE)
    except FileNotFoundError:
        print(DATASET_PATH)
        print("Failed to find Processed Dataset.\nPlease follow the README instructions to fetch and process the dataset")
    wavelengths = hyper_bands['Band_nanometers']
    noise_flags = hyper_bands['Noise_flag']
    hyper_image = loadmat(HYPER_FOLDER_PATH +
                          hyper_files[args.img_id])['image']

    if args.trim_image:
        plot_bands(wavelengths=trim_bands(wavelengths, noise_flags),
                   intensities=trim_bands(hyper_image[args.x][args.y], noise_flags))
    else:
        if args.trim_w:
            plot_bands(wavelengths=trim_bands(wavelengths, noise_flags),
                       intensities=hyper_image[args.x][args.y])
        else:
            plot_bands(wavelengths=wavelengths,
                       intensities=hyper_image[args.x][args.y])
