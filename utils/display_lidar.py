from scipy.io import loadmat

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import argparse


from datapaths import LIDAR_FILE
plt.style.use('ggplot')




def get_parsed_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--pc-id', default='3', dest='pc_id', choices=[str(
        x) for x in range(1, 52) if x not in [12, 22, 23, 24, 45, 46, 47, 49]])
    args = parser.parse_args()
    args.pc_id = args.pc_id if len(args.pc_id) == 2 else '0' + args.pc_id
    return args

if __name__ == '__main__':
    args = get_parsed_arguments()
    
    image = loadmat(LIDAR_FILE + args.pc_id + '_chm.mat')['image']
    # print(image, image.min(), image.max())
    plt.imshow(image, cmap=cm.get_cmap('afmhot', 4), origin='lower')
    plt.title("LiDAR Canopy Height Model Map Res 1m2")
    plt.colorbar(ticks=np.linspace(image.min(), image.max(), 5))
    plt.show()
