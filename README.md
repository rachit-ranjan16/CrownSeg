# Crown Segmentation

Segment Tree Crowns from RGB, Hyperspectral and LiDAR Images using Clustering techniques

## Dataset

 [NIST DSE Plant Identification with NEON Remote Sensing Data](https://www.ecodse.org/)
- Training Inputs(GeoTIFF Format)
  - 37 RGB Images (320,320,3)
  - 43 Hyperspectral Images (80,80,420)
  - 43 LiDAR Images (80,80)
  - 43 LiDAR PointCloud 3D Maps (20665,20665,20665)
- Training Outputs 
  - ShapeFiles highlighting Tree Crowns for 70% of the input data 
- `hyper_bands.csv` containing noisy bands for hyperspectral images 

[Download Link](https://zenodo.org/record/867646#.W9z2W2hKiHs)  
Modify `~/utils/datapaths.py` accordingly as per extraction/unzip tool used.

The code expects Dataset to be extracted as `~/ECODSEdataset/ECODSEdataset/`

## Observations and Inferences

    - Most RGB Images either show a blur or tilt or both along with not matching with their hyperspectral and lidar counterparts
        - RGB Images Not Used
    - Higher bands seem to have noisy information attributing to poor sensor calibration
        - Smoothed out using convolutions
        - End noise clipped out
    - Three LiDAR Elevation Maps have missing data
        - Shape of (77,80) instead of (80,80)
        - Not used to create composite masks with ndvi information
        - Clustering outputs available along with NDVI

## Prerequisites

    - Ubuntu 18.04 LTS Recommended
        - Default Python3 installation  
        - Pip3 Installation
            - ```console 
               sudo apt-get -y -q install python3-pip
               ```
    - GDAL Installation(Ubuntu instructions only)
        - `sudo apt-get -y -q install gdal-bin`
        - `sudo apt-get -y -q install python3-numpy`
        - `sudo apt-get -y -q install python3-gdal`
    - Install Requirements
        - `pip3 install -r requirements.txt`

## Additional Information

### NDVI Reference Range

| NDVI       | Vegetation Type   |
|------------|-------------------|
| -1         | Water             |
| -0.1 - 0.1 | Rock/Dirt         |
| 0.2 - 0.4  | Shrubs/Grasslands |
|  >0.4      | Trees/Rainforests |

#### AppConfig

All Parameters used are present in `~/appConfig.ini` and can be modified as per need

#### Outputs

All Outputs are stored in `~/OUT/` following a similar filename pattern structure to the dataset

## Methodology

- [x] Convert all GeoTIFF Files into easy to access and modify matlab files (.mat)
  - `python3 utils/convert_to_mat.py --help`
    - `python3 utils/convert_to_mat.py --file-type=rgb`
    - `python3 utils/convert_to_mat.py --file-type=lidar`
    - `python3 utils/convert_to_mat.py --file-type=hyper`
- [x] View Images 
  - Hyperspectral Image Bands 
    - `python3 utils/display_bands --help`
        - `python3 utils/display_bands --image-id=23 -x=40 -y=25`
    - Add `--trim-wavelengths=False` until noisy bands have been purged from the hyperspectral images(executed in the following instruction)
- [x] Hyperspectral Image Dimensionality Reduction
  - Purge Noisy Bands and Smooth out intensities in the higher bands for all pixels in all images
    - `python3 utils/reduce_dimensionality.py --help`
        - `python3 utils/reduce_dimensionality.py`
- [x] Create Normalized Difference Vegetation Index(NDVI) for each hyperspectral image
  - `python3 utils/calculate_ndvi.py`
- [x] Convert created NDVI from .tif to .mat format
  - `python3 utils/convert_to_mat.py --file-type=ndvi`
- [x] Threshold NDVI for Rainforests/Trees to a binary image and use as a mask over LiDAR CHM to further segment LiDAR into tree or no tree - assists in differentiating further between trees and other artifacts
  - `python3 utils/create_ndvi_lidar_mask.py`
- Execute Clustering Algorithms on Images(store output labels in .mat files)
  - `python3 clustering.py`
    - [x] K Means
    - [x] Gaussian Mixture Model
    - [ ] Fuzzy C Means
    - [ ] Self Organizing Maps
    - [ ] Spectral Clustering
- [x] Put the composite NDVI + LiDAR CHM as a mask over the cluster labels ensuring everything except crowns is soft thresholded to zero
  - [x] `python3 mask_clusters.py`  

## Future Work 
- [ ] Being FCM, SOM and Spectral Clustering to working shape 
- [ ] Convert ShapeFile Training Outputs to Image and then a matrix for comparison with 
- [ ] Performance Evaluation 
  - [ ] Compare Output Labels with available shapefile outputs using Jaccard's Coefficient to fine tune clustering algorithms' hyperparameters 

