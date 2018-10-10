from scipy.io import loadmat
from spectral import imshow
import time
# TODO Figure out why this isn't working 
hyper_image = loadmat('OSBS_003_hyper.mat')['image']

imshow(hyper_image)
# time.sleep(60)