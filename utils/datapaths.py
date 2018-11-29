from os import sep
from os.path import abspath, dirname

CONFIG_FILE = dirname(dirname(abspath(__file__))) + sep + 'appConfig.ini'
MISSING_MASKS = dirname(
    dirname(abspath(__file__))) + sep + 'missing_masks.txt'
DATASET_PATH = dirname(dirname(abspath(__file__))) + sep + \
    'ECODSEdataset' + sep + 'ECODSEdataset' + sep + 'RSdata' + sep
HYPER_SOURCE_PATH = DATASET_PATH + 'hs' + sep
HYPER_FOLDER_PATH = HYPER_SOURCE_PATH + 'MAT' + sep
HYPER_ORIG_FOLDER_PATH = HYPER_SOURCE_PATH + 'MAT-Orig' + sep
NDVI_SOURCE_PATH = DATASET_PATH + 'ndvi' + sep 
NDVI_FOLDER_PATH = NDVI_SOURCE_PATH + 'MAT' + sep 
HYPER_BANDS_FILE = dirname(dirname(abspath(__file__))) + sep + \
    'ECODSEdataset' + sep + 'ECODSEdataset' + sep+'hyper_bands.csv'
RGB_SOURCE_PATH = DATASET_PATH + 'camera' + sep
RGB_FOLDER_PATH = RGB_SOURCE_PATH + 'MAT' + sep
LIDAR_SOURCE_PATH = DATASET_PATH + 'chm' + sep
LIDAR_FOLDER_PATH = LIDAR_SOURCE_PATH + 'MAT' + sep
LIDAR_NORMALIZED_FOLDER_PATH = DATASET_PATH + 'chm' + sep + 'MAT-Normalized' + sep
NDVI_LIDAR_SOURCE_PATH = DATASET_PATH + 'ndvi_lidar' + sep
NDVI_LIDAR_FOLDER_PATH = NDVI_LIDAR_SOURCE_PATH + 'MAT' + sep
LIDAR_FILE = LIDAR_FOLDER_PATH + 'OSBS_0'
POINT_CLOUD_FILE = DATASET_PATH + 'pointCloud' + sep + 'ptcloud_OSBS_0'
