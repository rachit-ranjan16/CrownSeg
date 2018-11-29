from sklearn.cluster import KMeans, SpectralClustering
from sklearn.decomposition import PCA
from sklearn.mixture import GaussianMixture
from skimage.transform import pyramid_expand, pyramid_reduce, resize
from configparser import ConfigParser
from scipy.io import savemat, loadmat



import skfuzzy as skf
import spectral as sp
import numpy as np
import sompy
import logging

from utils.datapaths import CONFIG_FILE, HYPER_FOLDER_PATH, OUT_PATH,KMEANS_FOLDER_PATH, FCM_FOLDER_PATH, GMM_FOLDER_PATH, SOM_FOLDER_PATH, SPECTRAL_FOLDER_PATH
from commons import get_mat_file_names, clean_create
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(lineno)d:%(message)s')
log = logging.getLogger(__file__)

config = ConfigParser()
config.read(CONFIG_FILE)

def k_means_clustering(inp_image, n_clusters=int(config['KMEANS']['N_CLUSTERS'])):
    if inp_image is None:
        print("Empty Input. Exiting")
        return None
    # Create K Means Model
    k_means = KMeans(n_clusters=n_clusters)
    shape = inp_image.shape
    # Fit on Input Image
    k_means.fit(inp_image.flatten().reshape(shape[0]*shape[1], shape[2]))
    # Get Cluster Labels
    clust = k_means.labels_.astype(float)

    return clust.reshape(shape[0], shape[1])


def fuzzy_c_means(inp_image, n_clusters=int(config['FCM']['N_CLUSTERS'])):
    if inp_image is None:
        print("Empty Input. Exiting")
        return

    shape = inp_image.shape
    # Create and Train on FCM Model
    centers, u, u0, d, jm, n_iters, fpc = skf.cluster.cmeans(
        inp_image.flatten().reshape(shape[0]*shape[1], shape[2]).T,
        c=n_clusters,
        m=float(config['FCM']['FUZZ_DEGREE']),
        error=float(config['FCM']['ERROR']),
        maxiter=int(config['FCM']['MAX_ITER']),
        init=None,
        seed=int(config['FCM']['SEED'])
    )
    # Get Cluster Labels with Max Probability
    clust = np.argmax(u, axis=0).astype(float)

    return clust.reshape(shape[0], shape[1])


def gaussian_mixture_model(inp_image, n_clusters=int(config['KMEANS']['N_CLUSTERS'])):
    shape = inp_image.shape
    inp_image = inp_image.flatten().reshape(shape[0]*shape[1], shape[2])
    # Create Gaussian Mixture Model with Config Parameters
    gmm = GaussianMixture(
        n_components=n_clusters, covariance_type=config['GMM']['COVARIANCE_TYPE'],
        max_iter=int(config['GMM']['MAX_ITER']), random_state=int(config['GMM']['RANDOM_STATE']))
    # Fit on Input Image
    gmm.fit(X=inp_image)
    # Get Cluster Labels
    clust = gmm.predict(X=inp_image)

    return clust.reshape(shape[0], shape[1])


def spectral_cluster(inp_image, n_clusters=int(config['SPECTRAL']['N_CLUSTERS'])):
    original_shape = inp_image.shape
    downsampled_img = pyramid_reduce(inp_image, 3)
    shape = downsampled_img.shape
    downsampled_img = downsampled_img.reshape(shape[0]*shape[1], shape[2])
    sp = SpectralClustering(n_clusters=n_clusters,
                            eigen_solver=config['SPECTRAL']['EIGEN_SOLVER'],
                            affinity=config["SPECTRAL"]["AFFINITY"])
    sp.fit_predict(downsampled_img)
    clust = sp.labels_
    clust = clust.reshape(shape[0], shape[1])
    # Performimg kmeans to re generate clusters after resize, original segmentation remains intact.
    clust = k_means_clustering(n_clusters, resize(
        clust, (original_shape[:-1])).reshape((original_shape[:-1])+(1,)))
    return clust


def SOM(inp_image, n_clusters=int(config['SOM']['N_CLUSTERS']), n_job=int(config['SOM']['N_JOB']), map_dim=int(config['SOM']['MAP_DIM'])):

    # Calculate the map
    mapsize = [map_dim, map_dim]
    shape = inp_image.shape
    data = inp_image.flatten().reshape(shape[0]*shape[1], shape[2])
    som = sompy.SOMFactory.build(data, mapsize)
    som.train(n_job=n_job, verbose=None)

    # calculating clusters
    cl = som.cluster(n_clusters=n_clusters)

    # calculating which pixel is associated which cluster
    project_data = som.project_data(data)
    clust = np.zeros((shape[0], shape[1]))
    for i, q in enumerate(project_data):
        temp = cl[q]
        clust[np.unravel_index(i, dims=((shape[0], shape[1])))] = temp

    return clust


if __name__ == "__main__":

    algorithms = config['CLUSTERING']['ALGORITHMS'].split(',')

    clean_create(OUT_PATH[:-1])
    for algo in algorithms:
        log.info('Algorithm=%s', algo)
        if algo == 'KMeans':
            log.info('KMeans Clustering')
            clean_create(KMEANS_FOLDER_PATH[:-1])
            for hyper_file in get_mat_file_names(HYPER_FOLDER_PATH):
                log.debug('Tacking File=%s', hyper_file)
                savemat(KMEANS_FOLDER_PATH + 'OUT_' + hyper_file,
                        {'image': k_means_clustering(loadmat(HYPER_FOLDER_PATH + hyper_file)['image'])})
                exit(123)
        elif algo == 'FCM':
            clean_create(FCM_FOLDER_PATH[:-1])
            log.info('FCM Clustering')
            for hyper_file in get_mat_file_names(HYPER_FOLDER_PATH):
                log.debug('Tacking File=%s', hyper_file)
                savemat(FCM_FOLDER_PATH + 'OUT_' + hyper_file,
                        {'image': fuzzy_c_means(loadmat(HYPER_FOLDER_PATH + hyper_file)['image'])})
        elif algo == 'SOM':
            clean_create(SOM_FOLDER_PATH[:-1])
            log.info('Self Organizing Map Clustering')
            for hyper_file in get_mat_file_names(HYPER_FOLDER_PATH):
                log.debug('Tacking File=%s', hyper_file)
                savemat(SOM_FOLDER_PATH + 'OUT_' + hyper_file,
                        {'image': SOM(loadmat(HYPER_FOLDER_PATH + hyper_file)['image'])})
        elif algo == 'GMM':
            clean_create(GMM_FOLDER_PATH[:-1])
            log.info('Gaussian Mixture Model Clustering')
            for hyper_file in get_mat_file_names(HYPER_FOLDER_PATH):
                log.debug('Tacking File=%s', hyper_file)
                savemat(GMM_FOLDER_PATH + 'OUT_' + hyper_file,
                        {'image': gaussian_mixture_model(loadmat(HYPER_FOLDER_PATH + hyper_file)['image'])})
        elif algo == 'Spectral':
            clean_create(SPECTRAL_FOLDER_PATH[:-1])
            log.info('Spectral Clustering')
            for hyper_file in get_mat_file_names(HYPER_FOLDER_PATH):
                log.debug('Tacking File=%s', hyper_file)
                savemat(SPECTRAL_FOLDER_PATH + 'OUT_' + hyper_file,
                        {'image': spectral_cluster(loadmat(HYPER_FOLDER_PATH + hyper_file)['image'])})
    log.info('Execution Complete')
