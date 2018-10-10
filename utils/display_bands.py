import argparse
from os import sep, listdir
from os.path import isfile, join, dirname, abspath
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
from scipy.io import loadmat
import pandas as pd
import spectral as sp 

DATASET_PATH = dirname(dirname(abspath(
    __file__))) + sep +  'ECODSEdataset' + sep + 'ECODSEdataset' + sep + 'RSdata' + sep
HYPER_FOLDER_PATH = DATASET_PATH + 'hs' + sep + 'MAT' + sep
HYPER_BANDS_FILE = dirname(dirname(abspath(
    __file__))) + sep + 'ECODSEdataset' + sep + \
    'ECODSEdataset' + sep + 'hyper_bands.csv'

def plot_bands(wavelengths, intensities):
    f, ax = plt.subplots(1,1)
    ax.plot(wavelengths, intensities)
    f.set_title('')
    plt.show()


def trim_bands(source_list, flags):
    trimmed = []
    for i in range(len(flags)):
        if flags[i] == 0:
            trimmed.append(source_list[i])
    return trimmed


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--image-id', default=3, dest='img_id', 
                        choices=[str(x) for x in range(1, 52)])
    parser.add_argument('-x', default=40, dest='x', help='X coordinate less than 80')
    parser.add_argument('-y', default=25, dest='y', help='Y coordinate less than 80')
    parser.add_argument('--trim', default=False, dest='trim', help='Set to True if noisy bands need to be removed')
    args = parser.parse_args() 
    args.x = int(args.x)
    args.y = int(args.y)
    args.trim = bool(args.trim)
    try:
        hyper_files = sorted([hyper_file for hyper_file in
                            [f for f in listdir(HYPER_FOLDER_PATH) if isfile(join(HYPER_FOLDER_PATH, f))]])
        hyper_bands = pd.read_csv(HYPER_BANDS_FILE)
    except FileNotFoundError:
        print(DATASET_PATH)
        print("Failed to find Processed Dataset.\nPlease follow the README instructions to fetch and process the dataset")
    wavelengths = hyper_bands['Band_nanometers']
    noise_flags = hyper_bands['Noise_flag']
    hyper_image = loadmat(HYPER_FOLDER_PATH + hyper_files[args.img_id])['image']
    
    if args.trim is False: 
        plot_bands(wavelengths=wavelengths, intensities=hyper_image[args.x][args.y])
    else:
        plot_bands(wavelengths=trim_bands(wavelengths, noise_flags),
        intensities=trim_bands(hyper_image[args.x][args.y], noise_flags))
