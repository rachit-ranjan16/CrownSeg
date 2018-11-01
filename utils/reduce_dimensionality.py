import argparse
from os import listdir
from os.path import isfile, join
from scipy.io import loadmat, savemat
from configparser import ConfigParser

import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import logging


from datapaths import DATASET_PATH, HYPER_BANDS_FILE, HYPER_FOLDER_PATH, CONFIG_FILE

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(lineno)d:%(message)s')
log = logging.getLogger(__file__)


def trim_bands(source_list, filter_list):
    trimmed = []
    for i in range(len(filter_list)):
        if filter_list[i] == 0:
            trimmed.append(source_list[i])
    return trimmed

def smoothen(y, box_pts):
    return np.convolve(y, np.ones(box_pts)/box_pts, mode='same')

def smoothen_hyper_image(image):
    pos = int(config['RED_DIM']['SMOOTH_START_POS'])
    conv_size = int(config['RED_DIM']['CONV_SIZE'])
for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            image[i][j] = np.append(
                image[i][j][:pos], smoothen(image[i][j][pos:], conv_size))
    return image 

    
def smoothen_hyper_images():
    #TODO Change this to work on all files 
    for hyper_file in hyper_files:
        smooth_image = smoothen_hyper_image(
            loadmat(HYPER_FOLDER_PATH + hyper_file)['image'])
        savemat(HYPER_FOLDER_PATH + hyper_file, {'image': smooth_image})

def purge_noisy_bands(image, band_filter):
    # 369 usable bands per pixel
    out = np.zeros([80, 80, 369])
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            out[i][j] = trim_bands(image[i][j], band_filter)
    return out


def get_configured_parser():
    parser = argparse.ArgumentParser()
    #TODO Decide whether to keep or ditch this - Use matlab scripts to make this happen 
    # parser.add_argument('--merge-bands', default=False, dest='merge_bands',
    #                     help='Merge bands with averaging for bands with low symmetric KL Divergence')
    parser.add_argument('--smoothen-only', default=False, dest='smoothen_only',
                        help='Turns on only smoothing of reduced dimensionality data across bands for all images from the configured starting position')
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
    for hyper_file in hyper_files:
        clean_image = smoothen_hyper_image(purge_noisy_bands(
            loadmat(HYPER_FOLDER_PATH + hyper_file)['image'], hyper_bands['Noise_flag']))
        savemat(HYPER_FOLDER_PATH + hyper_file, {'image': clean_image})
        
# Maximal/Minimal Noise Fraction
# Generate documentation out of code automatically 
# NDVI Normalized Differential Vegetation Index 

# Standard deviation in crown areas. 
if __name__ == '__main__':
    log.info('Starting Execution')
    config = ConfigParser() 
    config.read(CONFIG_FILE)

    # TODO Decide whether this is needed after using COTS for KL Divergence based dimensionality reduction
    parser = get_configured_parser()
    args = parser.parse_args()
    # args.merge_bands = bool(args.merge_bands)
    args.smoothen_only = bool(args.smoothen_only)

    hyper_files, hyper_bands = fetch_file_names()
    log.info('Fetched all the Hyperspectral File Names')
    if args.smoothen_only and bool(config['RED_DIM']['SMOOTHEN']):
        log.info('Just Smoothening Hyper Images')
        smoothen_hyper_images()
        log.info('Execution Completed')
        exit(123)

    log.info('Attempting to Clean off all the noisy bands and smoothen the curves')
    clean_hyper_images()

    # if args.merge_bands:
    #     # TODO Add Band Merging using KL Divergence here
    #     pass
    log.info('Execution Completed')
