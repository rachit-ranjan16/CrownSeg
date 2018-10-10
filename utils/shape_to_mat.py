import gdal
import ogr
import osr
import numpy as np

# TODO Generalize, Cleanup and add Documentation
# TODO Figure out if this is necessary
RASTER_PATH = 'temp.tif'
# source_ds = ogr.Open("ITC_OSBS_003.shp")
# source_layer = source_ds.GetLayer()
# print (source_layer)
# pixelWidth = pixelHeight = 1
# x_min, x_max, y_min, y_max = source_layer.GetExtent()
# cols = int((x_max - x_min) / pixelHeight)
# rows = int((y_max - y_min) / pixelWidth)
# target_ds = gdal.GetDriverByName('GTiff').Create(
#     'temp.tif', cols, rows, 1, gdal.GDT_Byte)
# target_ds.SetGeoTransform((x_min, pixelWidth, 0, y_min, 0, pixelHeight))
# band = target_ds.GetRasterBand(1)
# NoData_value = 255
# band.SetNoDataValue(NoData_value)
# band.FlushCache()
# gdal.RasterizeLayer(target_ds, [1], source_layer, options=["ATTRIBUTE=confidence"])
# target_dsSRS = osr.SpatialReference()
# target_dsSRS.ImportFromEPSG(4326)
# target_ds.SetProjection(target_dsSRS.ExportToWkt())


def layer(shapefile):

    # 1) opening the shapefile
    source_ds = ogr.Open(shapefile)
    source_layer = source_ds.GetLayer()

    # 2) Creating the destination raster data source

    pixelWidth = pixelHeight = 1  # depending how fine you want your raster
    x_min, x_max, y_min, y_max = source_layer.GetExtent()
    cols = int((x_max - x_min) / pixelHeight)
    rows = int((y_max - y_min) / pixelWidth)
    target_ds = gdal.GetDriverByName('GTiff').Create(
        RASTER_PATH, cols, rows, 1, gdal.GDT_Byte)
    target_ds.SetGeoTransform((x_min, pixelWidth, 0, y_min, 0, pixelHeight))
    band = target_ds.GetRasterBand(1)
    NoData_value = 255
    band.SetNoDataValue(NoData_value)
    band.FlushCache()

    # 4) Instead of setting a general burn_value, use optionsand set it to the attribute that contains the relevant unique value ["ATTRIBUTE=ID"]
    gdal.RasterizeLayer(target_ds, [1], source_layer, options=[
                        'ATTRIBUTE=crown_id'])

    # 5) Adding a spatial reference
    target_dsSRS = osr.SpatialReference()
    target_dsSRS.ImportFromEPSG(2975)
    target_ds.SetProjection(target_dsSRS.ExportToWkt())
    return gdal.Open(RASTER_PATH).ReadAsArray()


out = np.array(layer("ITC_OSBS_003.shp"))
print(out.shape)
print(out)
