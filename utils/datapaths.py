from os import sep
from os.path import abspath, dirname

DATASET_PATH = dirname(dirname(abspath(__file__))) + sep + \
    'ECODSEdataset' + sep + 'ECODSEdataset' + sep + 'RSdata' + sep
HYPER_FOLDER_PATH = DATASET_PATH + 'hs' + sep + 'MAT' + sep
HYPER_BANDS_FILE = dirname(dirname(abspath(__file__))) + sep + \
    'ECODSEdataset' + sep + 'ECODSEdataset' + sep+'hyper_bands.csv'
RGB_FOLDER_PATH = DATASET_PATH + 'camera' + sep
LIDAR_FOLDER_PATH = DATASET_PATH + 'chm' + sep
