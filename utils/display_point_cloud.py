from mpl_toolkits.mplot3d import Axes3D
from os import sep
from os.path import join, dirname, abspath
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import argparse

# POINT_CLOUD_FILE = dirname(dirname(abspath(
#     __file__))) + sep  + 'ECODSEdataset' + sep + 'ECODSEdataset' + sep + 'RSdata' + \
#     sep + 'pointCloud' + sep + 'ptcloud_OSBS_0'
from datapaths import POINT_CLOUD_FILE

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--pc-id', default='3', dest='pc_id', choices=[str(
        x) for x in range(1, 52) if x not in [12, 22, 23, 24, 45, 46, 47, 49]])
    args = parser.parse_args()
    args.pc_id = args.pc_id if len(args.pc_id) == 2 else '0' + args.pc_id
    pc_df = pd.read_csv(POINT_CLOUD_FILE + args.pc_id + '.csv')
    # TODO Figure out whether Normalization is necessary??
    # pc_df['Z']/= max(pc_df['Z'])
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    X = np.array(pc_df['X'])
    Y = np.array(pc_df['Y'])
    Z = np.array(pc_df['Z'])
    surf = ax.plot_trisurf(X, Y, Z,
                           linewidth=0.8, antialiased=True)
    plt.show()
