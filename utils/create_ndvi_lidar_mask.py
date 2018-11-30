from os import mkdir
from shutil import rmtree
from scipy.io import loadmat, savemat
from scipy.ndimage import median_filter
from configparser import ConfigParser

import cv2
import logging

from datapaths import DATASET_PATH, NDVI_FOLDER_PATH, LIDAR_FOLDER_PATH, CONFIG_FILE, NDVI_LIDAR_SOURCE_PATH, NDVI_LIDAR_FOLDER_PATH

from commons import get_mat_file_names, clean_create

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(lineno)d:%(message)s')
log = logging.getLogger(__file__)


def generate_lidar_ndvi_mask(lidar, ndvi):
    threshold = float(config['NDVI']['THRESHOLD'])
    ndvi[ndvi < threshold] = 0
    ndvi[ndvi > threshold] = 1

    return median_filter(cv2.bitwise_and(src1=lidar.astype(int), src2=ndvi.astype(int)), size=int(config['MEDIAN_FILTER']['WINDOW_SIZE']))


if __name__ == '__main__':
    config = ConfigParser()
    config.read(CONFIG_FILE)

    lidar_files = get_mat_file_names(LIDAR_FOLDER_PATH)
    ndvi_files = get_mat_file_names(NDVI_FOLDER_PATH)

    try:
        # Create Output Directory
        mkdir(NDVI_LIDAR_SOURCE_PATH[:-1])
    except FileExistsError:
        log.debug('Output Directory Exists.')

    clean_create(NDVI_LIDAR_FOLDER_PATH[:-1])

    for i in range(len(lidar_files)):

        log.debug('Tackling LidarFile=%r NdviFile=%r',
                  lidar_files[i], ndvi_files[i])
        lidar = loadmat(LIDAR_FOLDER_PATH + lidar_files[i])['image']
        ndvi = loadmat(NDVI_FOLDER_PATH + ndvi_files[i])['image']
        if lidar.shape != ndvi.shape:
            log.warning('Corrupted %s or %s. Skipping the pair',
                        lidar_files[i], ndvi_files[i])
            continue
        lidar_ndvi = generate_lidar_ndvi_mask(lidar, ndvi)
        f = lidar_files[i]
        savemat(NDVI_LIDAR_FOLDER_PATH +
                f[:f[::-1].find('_') + 2] + 'ndvi_lidar.mat', {'image': lidar_ndvi})

    log.info('Execution Complete')
