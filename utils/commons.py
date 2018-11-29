from os import listdir, mkdir
from os.path import isfile, join
from shutil import rmtree

import logging

from datapaths import MISSING_MASKS

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(lineno)d:%(message)s')
log = logging.getLogger(__file__)


def get_file_names(source_path):
    return sorted([f for f in
                   [f for f in listdir(source_path) if isfile(
                       join(source_path, f))]
                   if 'tif' in f and 'aux.xml' not in f])


def get_mat_file_names(source_path):
    return sorted([f for f in listdir(source_path) if isfile(join(source_path, f))])


def put_missing_mask_indices(cor_ind):
    with open(MISSING_MASKS, mode='w') as f:
        f.write(str(cor_ind))


def get_missing_mask_indices():
    with open(MISSING_MASKS, mode='w') as f:
        return f.read().replace('[', '').replace(']', '').split(', ')


def clean_create(path):
    log.debug('Clearing out %s recursively', path)
    try:
        rmtree(path)
    except FileNotFoundError:
        log.debug("Out Directory doesn't exist")
    log.debug('Creating directory at path=%s', path)
    mkdir(path)