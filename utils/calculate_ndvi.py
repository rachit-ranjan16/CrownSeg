#! /usr/bin/env python

from configparser import ConfigParser
from os import listdir, mkdir
from os.path import isfile, join
from shutil import rmtree

import sys
import os
import struct
import osgeo.gdal as gdal
import argparse
import logging

from datapaths import DATASET_PATH, HYPER_BANDS_FILE, HYPER_SOURCE_PATH, CONFIG_FILE, NDVI_SOURCE_PATH
# TODO Pull from commons after refactoring
from convert_to_mat import get_file_names

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(lineno)d:%(message)s')
log = logging.getLogger(__file__)


class GDALCalcNDVI():

    def createOutputImage(self, outFilename, inDataset):
        '''
            Creates Output Image
        '''
        # Define the image driver to be used
        # This defines the output file format (e.g., GeoTiff)
        driver = gdal.GetDriverByName("GTiff")
        # Check that this driver can create a new file.
        metadata = driver.GetMetadata()
        if gdal.DCAP_CREATE in metadata and metadata[gdal.DCAP_CREATE] != 'YES':
            log.error('Driver GTIFF does not support Create()')
            sys.exit(-1)
        # Get the spatial information from the input file
        geoTransform = inDataset.GetGeoTransform()
        geoProjection = inDataset.GetProjection()
        # Create an output file of the same size as the inputted
        # image but with only 1 output image band.
        newDataset = driver.Create(outFilename, inDataset.RasterXSize,
                                   inDataset.RasterYSize, 1, gdal.GDT_Float32)
        # Define the spatial information for the new image.
        newDataset.SetGeoTransform(geoTransform)
        newDataset.SetProjection(geoProjection)
        return newDataset

    def calcNDVI(self, in_file, out_file):
        '''
            The function which loops through the input image and calculates the output NDVI value to be outputted.
        '''
        # Open the input dataset
        dataset = gdal.Open(in_file, gdal.GA_ReadOnly)
        # Check the dataset was successfully opened
        if dataset is None:
            log.error("The dataset could not openned")
            sys.exit(-1)

        # Create the output dataset
        outDataset = self.createOutputImage(out_file, dataset)
        # Check the datasets was successfully created.
        if outDataset is None:
            log.error('Could not create output image')
            sys.exit(-1)

        # Get hold of the RED and NIR image bands from the image
        red_band = dataset.GetRasterBand(
            int(config['NDVI']['RED_BAND']))  # RED BAND
        nir_band = dataset.GetRasterBand(
            int(config['NDVI']['NIR_BAND']))  # NIR BAND
        # Retrieve the number of lines within the image
        numLines = red_band.YSize
        # Loop through each line in turn.
        for line in range(numLines):
            # Define variable for output line.
            outputLine = b''
            # Read in data for the current line from the
            # image band representing the red wavelength
            red_scanline = red_band.ReadRaster(0, line, red_band.XSize, 1,
                                               red_band.XSize, 1, gdal.GDT_Float32)
            # Unpack the line of data to be read as floating point data
            red_tuple = struct.unpack('f' * red_band.XSize, red_scanline)

            # Read in data for the current line from the
            # image band representing the NIR wavelength
            nir_scanline = nir_band.ReadRaster(0, line, nir_band.XSize, 1,
                                               nir_band.XSize, 1, gdal.GDT_Float32)
            # Unpack the line of data to be read as floating point data
            nir_tuple = struct.unpack('f' * nir_band.XSize, nir_scanline)

            # Loop through the columns within the image
            for i in range(len(red_tuple)):
                # Calculate the NDVI for the current pixel.
                ndvi_lower = (nir_tuple[i] + red_tuple[i])
                ndvi_upper = (nir_tuple[i] - red_tuple[i])
                ndvi = 0
                if ndvi_lower == 0:
                    ndvi = 0
                else:
                    ndvi = ndvi_upper/ndvi_lower
                # Add the current pixel to the output line
                # log.info(ndvi, type(ndvi))
                outputLine = b''.join([outputLine, struct.pack('f', ndvi)])
            # Write the completed line to the output image
            outDataset.GetRasterBand(1).WriteRaster(0, line, red_band.XSize, 1,
                                                    outputLine, buf_xsize=red_band.XSize,
                                                    buf_ysize=1, buf_type=gdal.GDT_Float32)
            # Delete the output line following write
            del outputLine


if __name__ == '__main__':
    config = ConfigParser()
    config.read(CONFIG_FILE)
    ndvi = GDALCalcNDVI()
    try:
        hyper_files = get_file_names(HYPER_SOURCE_PATH)
    except FileNotFoundError:
        print(DATASET_PATH)
        print("Failed to find Source Dataset")
        exit(123)

    log.info('Deleting Output Directory Contents if any exists recursively')
    # TODO Refactor to commons
    try:
        rmtree(DATASET_PATH + 'NDVI')
    except FileNotFoundError as e:
        log.info("Out Directory doesn't exist. Gonna create one.")
    # Create Output Directory
    mkdir(DATASET_PATH + 'NDVI')

    log.info('Processing HyperFiles to figure out corresponding NDVI')
    for hyper_file in hyper_files:
        log.debug('Tackling HyperFile=%r', hyper_file)
        ndvi.calcNDVI(HYPER_SOURCE_PATH + hyper_file, NDVI_SOURCE_PATH +
                      hyper_file.split('.')[0] + '_ndvi.' + hyper_file.split('.')[1])
        log.debug('NDVI of HyperFile=%s saved', hyper_file)
    log.info(
        'Execute python ~/utils/convert_to_mat.py --file-type=ndvi to convert to .mat format')
