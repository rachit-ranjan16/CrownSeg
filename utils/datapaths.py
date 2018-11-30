from os import sep
from os.path import abspath, dirname


CONFIG_FILE = dirname(dirname(abspath(__file__))) + sep + 'appConfig.ini'

DATASET_PATH = dirname(dirname(abspath(__file__))) + sep + \
    'ECODSEdataset' + sep + 'ECODSEdataset' + sep + 'RSdata' + sep
HYPER_SOURCE_PATH = DATASET_PATH + 'hs' + sep
HYPER_FOLDER_PATH = HYPER_SOURCE_PATH + 'MAT' + sep
NDVI_SOURCE_PATH = DATASET_PATH + 'ndvi' + sep
NDVI_FOLDER_PATH = NDVI_SOURCE_PATH + 'MAT' + sep
HYPER_BANDS_FILE = dirname(dirname(abspath(__file__))) + sep + \
    'ECODSEdataset' + sep + 'ECODSEdataset' + sep+'hyper_bands.csv'
RGB_SOURCE_PATH = DATASET_PATH + 'camera' + sep
RGB_FOLDER_PATH = RGB_SOURCE_PATH + 'MAT' + sep
LIDAR_SOURCE_PATH = DATASET_PATH + 'chm' + sep
LIDAR_FOLDER_PATH = LIDAR_SOURCE_PATH + 'MAT' + sep
NDVI_LIDAR_SOURCE_PATH = DATASET_PATH + 'ndvi_lidar' + sep
NDVI_LIDAR_FOLDER_PATH = NDVI_LIDAR_SOURCE_PATH + 'MAT' + sep
LIDAR_FILE = LIDAR_FOLDER_PATH + 'OSBS_0'
POINT_CLOUD_FILE = DATASET_PATH + 'pointCloud' + sep + 'ptcloud_OSBS_0'

OUT_PATH = dirname(dirname(abspath(__file__))) + sep + 'OUT' + sep
KMEANS_FOLDER_PATH = OUT_PATH + sep + 'KMeans' + sep
KMEANS_MASKED_FOLDER_PATH = KMEANS_FOLDER_PATH + 'Masked' + sep
FCM_FOLDER_PATH = OUT_PATH + sep + 'FCM' + sep
FCM_MASKED_FOLDER_PATH = FCM_FOLDER_PATH + 'Masked' + sep
GMM_FOLDER_PATH = OUT_PATH + sep + 'GMM' + sep
GMM_MASKED_FOLDER_PATH = GMM_FOLDER_PATH + 'Masked' + sep
SOM_FOLDER_PATH = OUT_PATH + sep + 'SOM' + sep
SOM_MASKED_FOLDER_PATH = SOM_FOLDER_PATH + 'Masked' + sep
SPECTRAL_FOLDER_PATH = OUT_PATH + sep + 'Spectral' + sep
SPECTRAL_MASKED_FOLDER_PATH = SPECTRAL_FOLDER_PATH + 'Masked' + sep
