from os import listdir, mkdir
from os.path import isfile, join

import argparse
import shapefile
import matplotlib.pyplot as plt
import numpy as np
# TODO Generalize

from datapaths import TRAIN_OUT_SHAPES_FOLDER_PATH

SHAPE_FILE_PREFIX = 'ITC_OSBS_0'
plt.style.use('ggplot')

def get_parsed_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--pc-id', default='3', dest='pc_id', choices=[str(
        x) for x in range(1, 52) if x not in [2, 4, 5, 12, 13, 20, 21, 22, 23, 24, 27, 28, 31, 39, 40, 41, 45, 46, 47, 49, 50]])
    args.pc_id = args.pc_id if len(args.pc_id) == 2 else '0' + args.pc_id
    return parser.parse_args()    


if __name__ == "__main__":
    args = get_parsed_args() 
    
    sf = shapefile.Reader(TRAIN_OUT_SHAPES_FOLDER_PATH  +
                           SHAPE_FILE_PREFIX + args.pc_id)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    for shape in sf.shapes():
        x = np.array([i[0] for i in shape.points[:]])
        y = np.array([i[1] for i in shape.points[:]])
        plt.plot(x,y)

    print("Displaying Polygons")
    plt.show()

