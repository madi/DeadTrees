__author__ = "Laura Martinez Sanchez, Margherita Di Leo"
__license__ = "GPL v.3"
__version__ = "2.0"
__email__ = "lmartisa@gmail.com, dileomargherita@gmail.com"

import os
import ctypes
from osgeo import gdal, gdalnumeric, ogr, osr
from osgeo import gdal_array
import numpy as np
import time
import re


#-------------------------------------------------------------------------------
# DONE: added argument 'file' to pass the root name of the file
def ListTextureLayers(texturepath, file):
    '''This function compares the file basename with the lists of all the texture
    layers present in the folder, and lists the ones that match with the file name
    '''
    texturelist = []




    # DONE: added a check for texture name matching the file root name
    for texture in os.listdir(str(texturepath)):
        match = re.search(file, texture)
        if match:
            texturelist.append(texture)
    return texturelist


#-------------------------------------------------------------------------------


def createTextureArray(texturepath, orthopath, file):
    texturelist = ListTextureLayers(texturepath, file)

    ortho = gdal.Open(orthopath)
    XOriginal = ortho.RasterXSize
    YOriginal = ortho.RasterYSize
    shpOriginal = [YOriginal, XOriginal]
    print shpOriginal
    projection = ortho.GetProjection()
    geotrans = ortho.GetGeoTransform()

    imgOriginal = gdal.GetDriverByName('MEM').Create('texturesmem.tif', \
                                                             XOriginal, \
                                                             YOriginal, \
                                                             4 + len(texturelist), \
                                                             gdal.GDT_UInt16)

    #add RGBNIR layers
    print "Reading Mosaic"
    imgOriginal.GetRasterBand(1).WriteArray(ortho.GetRasterBand(1).ReadAsArray())
    ortho.FlushCache()
    imgOriginal.GetRasterBand(2).WriteArray(ortho.GetRasterBand(2).ReadAsArray())
    ortho.FlushCache()
    imgOriginal.GetRasterBand(3).WriteArray(ortho.GetRasterBand(3).ReadAsArray())
    ortho.FlushCache()
    imgOriginal.GetRasterBand(4).WriteArray(ortho.GetRasterBand(4).ReadAsArray())
    ortho.FlushCache()
    ortho = None #free the memory

    for i in range(len(texturelist)):

        print "Reading " + str(texturelist[i])
        texture = gdal.Open(texturepath + os.sep + str(texturelist[i]))
        imgOriginal.GetRasterBand(i + 5).WriteArray((texture.GetRasterBand(1).ReadAsArray()).astype('uint16'))
        texture.FlushCache()
        texture = None

    #imgOriginal = np.concatenate(imgarray.T) #Transpose because of gdal
    imgOriginal.SetGeoTransform(geotrans)
    imgOriginal.SetProjection(projection)


    return imgOriginal, shpOriginal




























































































#
