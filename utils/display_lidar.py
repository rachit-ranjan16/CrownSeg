from scipy.io import loadmat

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import argparse
from datapaths import LIDAR_FILE

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--pc-id', default='3', dest='pc_id', choices=[str(
        x) for x in range(1, 52) if x not in [12, 22, 23, 24, 45, 46, 47, 49]])
    args = parser.parse_args()
    args.pc_id = args.pc_id if len(args.pc_id) == 2 else '0' + args.pc_id

    image = loadmat(LIDAR_FILE + args.pc_id + '_chm.mat')['image']
    plt.imshow(image, cmap=cm.get_cmap('afmhot', 4),
               vmin=0, vmax=1, origin='lower')
    plt.title("LiDAR Heat Map")
    plt.colorbar(ticks=np.linspace(0, 1, 5))
    plt.show()
