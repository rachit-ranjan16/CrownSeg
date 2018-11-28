from os import listdir
from os.path import isfile, join

def get_file_names(source_path):
    return sorted([f for f in
                   [f for f in listdir(source_path) if isfile(
                       join(source_path, f))]
                   if 'tif' in f and 'aux.xml' not in f])

def get_mat_file_names(source_path):
     return sorted([f for f in listdir(source_path) if isfile(join(source_path, f))])
