import argparse
import logging
from os import listdir, mkdir, rmdir, sep
from os.path import abspath, dirname, isfile, join
from shutil import rmtree

import numpy
from scipy.io import savemat

import gdal
from datapaths import DATASET_PATH

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(lineno)d:%(message)s')
log = logging.getLogger(__file__)

# TODO Refactor to commons 
def get_file_names(source_path):
    return sorted([f for f in
                   [f for f in listdir(source_path) if isfile(
                       join(source_path, f))]
                   if 'tif' in f and 'aux.xml' not in f])


def cast_to_mat(input_files, source_path, dest_path):
    log.info('Casting .tiff to .mat')
    for f in input_files:
        # Read GeoTIFF Hyperspectral Image Files
        image = gdal.Open(
            source_path + f).ReadAsArray().T
        # TODO Check whether gDAL Open is returning other information that might be useful. 
        # Check this and hyperspectral image for any coordinates that might help in conversion. 
        # Normalize if not LiDAR CHM
        if args.file_type != 'lidar':
            image /= image.max()
        # Write as .mat file
        savemat(dest_path + f.split('.')
                [0] + '.mat', {'image': image})


def get_configured_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file-type', default='hyper', dest='file_type',
                        choices=['rgb', 'hyper', 'lidar', 'ndvi'], help="rgb, hyper, lidar or ndvi(needs to be created first using calculate_ndvi.py)")
    return parser


if __name__ == "__main__":
    log.info('Starting Execution')
    parser = get_configured_parser()
    args = parser.parse_args()

    if args.file_type == 'hyper':
        # Read HyperImage filenames
        source_path = DATASET_PATH + 'hs' + sep
        input_files = get_file_names(source_path)

    elif args.file_type == 'lidar':
        # Read LIDAR filenames
        source_path = DATASET_PATH + 'chm' + sep
        input_files = get_file_names(source_path)
    elif args.file_type == 'rgb':
        # Read RGB filenames
        source_path = DATASET_PATH + 'rgb' + sep
        input_files = get_file_names(source_path)
    else: 
        # Read NDVI filenames 
        source_path = DATASET_PATH + 'NDVI' + sep 
        input_files = get_file_names(source_path)
    log.info('Deleting Output Directory Contents if any exist recursively')

    #TODO Refactor to commons 
    try:
        rmtree(source_path + 'MAT')
    except FileNotFoundError as e:
        log.info("Out Directory doesn't exist. Gonna create one.")
    # Create Output Directory
    mkdir(source_path + 'MAT')

    cast_to_mat(input_files, source_path, source_path + 'MAT' + sep)
    log.info('Execution Complete')
