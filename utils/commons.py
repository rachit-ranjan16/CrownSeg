from os import listdir
from os.path import isfile, join
from datapaths import MISSING_MASKS

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
