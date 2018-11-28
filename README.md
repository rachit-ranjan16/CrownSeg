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

## Observations and Inferences 
    - Most RGB Images either show a blur or tilt or both along with not matching with their hyperspectral and lidar counterparts 
        - RGB Images Not Used 
    - Higher bands seem to have noisy information attributing to poor sensor calibration
        - Smoothed out using convolutions 
        - End noise clipped out

## Prerequisites 
    TODO Add this along with setup instructions 

## Methodology
TODO Add relevant code execution lines with each instruction   
- Convert all GeoTIFF Files into easy to access and modify matlab files (.mat)
- Hyperspectral Image Operations 
    - Remove Noisy Bands 
    - Smooth out intensities in the higher bands for all pixels in all images 
- Execute Clustering Algorithms on Images(store output labels in .mat files) <br/>
  TODO Zone in on the ones to be used 
    - K Means 
    - Fuzzy C Means 
    - Gaussian Mixture Model 
    - Self Organizing Maps 
    - Hierarchical  
- Create Normalized Difference Vegetation Index(NDVI) for each hyperspectral image
    - Ranges from -1(water) to 1(rainforests)
    - Convert created NDVI from .tif to .mat format
- Threshold NDVI for Rainforests/Trees to a binary image and use as a mask over LiDAR CHM to further segment LiDAR into tree or no tree - assists in differentiating further between trees and other artifacts
- Put the composite NDVI + LiDAR CHM as a mask over the cluster labels ensuring everything except crowns is soft thresholded to zero 
- Convert ShapeFile Training Outputs to Image and then a matrix for comparison with 
- Compare Output Labels with available shapefile outputs to fine tune clustering algorithms' hyperparameters 
