__author__ = "Laura Martinez Sanchez, Margherita Di Leo"
__license__ = "GPL v.3"
__version__ = "2.0"
__email__ = "lmartisa@gmail.com, dileomargherita@gmail.com"


from clipshape import *
from serialize import *
import os

# Information to provide:
field = "zona" # field in the shapefile where to read the classes
# The following is a subset of the ortophoto, in one file, to which the classes
# are referred
rasterPath  = "/home/madi/Projects/CasteloBranco/classification_test/trainingset/ortho/trainingset.tif"
# The following is a shapefile with polygons representing the various classes
shapePath   = "/home/madi/Projects/CasteloBranco/classification_test/trainingset/features/new_trainingset_features_20161222_5classes.shp"
# Path to the texture layers of the training set
texture_train_Path = "/home/madi/Projects/CasteloBranco/classification_test/trainingset/texture/"
INX = True
#pickleclip = "clipfeat-20161222_5classes"
pickleclip = "clipfeat-20161222_5classes_2text"

def init_texture(field, rasterPath, shapePath, INX, file, texture_train_Path, pickleclip):
    '''
    Create the initialization file (clip)
    '''

    feat, nPixels = ObtainPixelsfromShape(field, \
                                          rasterPath, \
                                          shapePath, \
                                          INX,\
                                          file, \
                                          texture_train_Path)
    # INX can be false. If True, uses additional layers.
    Mylist = [feat, nPixels] #pickle wants a list as input

    # Creates the folder if it doesn't exist
    if not os.path.exists("pickle/clip/"):
        os.makedirs("pickle/clip/")
    save("pickle/clip/" + pickleclip, Mylist)

init_texture(field, rasterPath, shapePath, INX, "trainingset", texture_train_Path, pickleclip)
