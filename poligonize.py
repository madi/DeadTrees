__author__ = "Laura Martinez Sanchez, Margherita Di Leo"
__license__ = "GPL"
__version__ = "2.0"
__email__ = "lmartisa@gmail.com, dileomargherita@gmail.com"


from osgeo import gdal, ogr,osr
import numpy as np
import time
from osgeo import gdal, gdalnumeric, ogr, osr,gdal_array
import os
import sys
import argparse


parser = argparse.ArgumentParser(description = "Performs prediction")
parser.add_argument('--rasterpath', dest = "rasterpath",
                                 help = "Input Path for the classified images")
parser.add_argument('--shapepath', dest = "shapepath",
                                 help = "Output Path for the classified polygons")
parser.add_argument('--product', dest = "product",
                                 help = "1 for dead trees (spiders), 6 for declining trees")


args = parser.parse_args()

rasterpath   = args.rasterpath
shapepath = args.shapepath
product = args.product


def GetRasterDataSource (name, rasterpath):

    src_ds = gdal.Open(rasterpath + name + '.tif')
    projection = src_ds.GetProjection()
    geotrans = src_ds.GetGeoTransform()
    XOriginal = src_ds.RasterXSize
    YOriginal = src_ds.RasterYSize
    shape = [YOriginal, XOriginal]

    if src_ds is None:
        print 'Unable to open %s' % src_filename
        sys.exit(1)

    try:
        srcband = src_ds.GetRasterBand(1)
    except RuntimeError, e:

        print 'Band ( %i ) not found' % band_num
        print e
        sys.exit(1)
    srcarray = src_ds.ReadAsArray()
    return srcarray,projection,geotrans, shape


def polygonize(shapepath, file, rasterpath):
    srcarray, projection, geotrans, shape = GetRasterDataSource(file, rasterpath)
    print "Start polygonizing.."
    start = time.time()
    if product == '1':
        srcarray[srcarray > 1] = 0 #we are interested in the class 1, we put everything else to 0
    elif product == '6':
        srcarray[srcarray < 6] = 0
    else:
        print "Product not available"

    drv = gdal.GetDriverByName('MEM')
    srs = osr.SpatialReference()
    srs.ImportFromWkt(projection)
    src_ds  = drv.Create('', shape[1], shape[0], 1, gdal.GDT_UInt16)
    src_ds.SetGeoTransform(geotrans)

    src_ds.SetProjection(projection)
    gdal_array.BandWriteArray(src_ds.GetRasterBand(1), srcarray)

    srcband = src_ds.GetRasterBand(1)

    drv = ogr.GetDriverByName("ESRI Shapefile")
    dst_ds = drv.CreateDataSource(shapepath + file + "_class" + product + ".shp")

    dst_layer = dst_ds.CreateLayer(shapepath + file, srs = srs)
    new_field = ogr.FieldDefn("type", ogr.OFTInteger)
    dst_layer.CreateField(new_field)

    new_field = None

    new_field = ogr.FieldDefn("area", ogr.OFTReal)

    # new_field.SetWidth(32)
    # new_field.SetPrecision(2) #added line to set precision (for floating point)
    dst_layer.CreateField(new_field)

    gdal.Polygonize(srcband, srcband, dst_layer, 0, [], callback = None )
    print "Number of features detected: ", dst_layer.GetFeatureCount()

    for feature in dst_layer:
        geom = feature.GetGeometryRef()
        area = geom.GetArea()
        feature.SetField("area", area)
        dst_layer.SetFeature(feature)

        # Filter per size
        if (geom.GetArea() < 1) or (geom.GetArea() > 100):
            dst_layer.DeleteFeature(feature.GetFID())


    dst_layer.SyncToDisk()
    dst_ds.ExecuteSQL("REPACK " + file + "_class" + product)

    print "Number of features after deleting: ", dst_layer.GetFeatureCount()
    dst_ds = None

    print "*---------------------------*"
    print "Shapefile correctly saved in: " + shapepath
    end = time.time()
    print "Time for polygonizing: "
    print (end-start)



def main(rasterpath, shapepath):
    for file in os.listdir(rasterpath):
        if file.endswith("_smooth.tif"):
            file = os.path.splitext(file)[0]
            print "Opening.. " + file + ".tif"
            polygonize(shapepath, file, rasterpath)


if __name__ == "__main__":
    main(rasterpath, shapepath)
