__author__ = "Laura Martinez Sanchez, Margherita Di Leo"
__license__ = "GPL v.3"
__version__ = "2.0"
__email__ = "lmartisa@gmail.com, dileomargherita@gmail.com"



from clipshape2 import *
from serialize import *
import itertools
#from mlh import *
from collections import defaultdict
import numpy as np
#from texture_initialize import *
import matplotlib.pyplot as plt
import os,sys
import glob
import argparse

'''
This code is used to establish the variability expressed by each texture layer
in each class
'''


feat = defaultdict(list)

#----------------------------------------------------------------------

def initialize(FIELD, INPUT_FOLDER, SHAPEPATH, TEXTURE, pickleclip):
    '''
    Create the initialization file (clip)
    '''

    INX = False
    rasterPath = INPUT_FOLDER + TEXTURE + ".tif"

    feat, nPixels = ObtainPixelsfromShape(FIELD, \
                                          rasterPath, \
                                          SHAPEPATH, \
                                          INX)

    print feat.keys()
    # INX can be false. If True, uses additional layers.
    Mylist = [feat, nPixels] #pickle wants a list as input

    # Creates the folder if it doesn't exist
    if not os.path.exists("pickle/clip/"):
        os.makedirs("pickle/clip/")
    save(pickleclip, Mylist)
    print "saved ", pickleclip


#----------------------------------------------------------------------

def myboxplot(title, data, median, deviation, categories, DESTINATION_FOLDER):


    fig = plt.figure()

    plt.boxplot(data, notch = True)

    plt.xticks([1, 2, 3, 4, 6], ["Spiders", "Healthy Tree", "Soil", "Shadow", "Declining Tree"])
    plt.title(title)

    print "Saving.. ", str(DESTINATION_FOLDER) + os.sep + str(title) + ".png"

    fig.savefig(str(DESTINATION_FOLDER) + os.sep + str(title) + ".png")

    # plt.show()


#----------------------------------------------------------------------

if __name__ == "__main__":

    ##---INPUT
    # parser
    parser = argparse.ArgumentParser(description = 'Calculates statistics of \
             representativeness of each class in the given texture')

    # path to input folder
    parser.add_argument('--textPath', dest = "textPath",
    help = "Folder where the input textures are. ")
    # example: '/home/madi/Projects/CasteloBranco/classification_test/trainingset/texture/'

    # path to shapefile folder
    parser.add_argument('--shapePath', dest = "shapePath",
    help = "Shapefile used as reference classification, path included. The shape \
            file contains the polygons representing each class. ")
    # example: '/home/madi/Projects/CasteloBranco/classification_test/trainingset/features/new_trainingset_features_20161222_5classes.shp'

    parser.add_argument('--field', dest = "field",
    help = "field in the shapefile where to read the classes. ")
    # example: 'zona'

    # path to output folder
    parser.add_argument('--outfolder', dest = "outfolder",
    help = "Destination folder where the graphics will be saved. ")
    # example: '/home/madi/Projects/CasteloBranco/classification_test/trainingset/stats/'

    parser.add_argument('--texture', dest = "texture",
    help = "texture file to process. ")
    # example: 'text_b1_trainingset_Contr'

    args = parser.parse_args()

    global INPUT_FOLDER
    global DESTINATION_FOLDER
    global TEXTURE
    global SHAPEPATH
    global FIELD

    INPUT_FOLDER = args.textPath
    DESTINATION_FOLDER = args.outfolder
    TEXTURE = args.texture
    SHAPEPATH = args.shapePath
    FIELD = args.field
    pickleclip = 'pickle/clip/' + TEXTURE



    print "Initializing.. ", pickleclip
    initialize(FIELD, INPUT_FOLDER, SHAPEPATH, TEXTURE, pickleclip)

    with open(pickleclip + '.pickle', 'rb') as handle:
        Mylist = pickle.load(handle)

        feat = Mylist[0]
        print "feat.keys()", feat.keys()

        temp = defaultdict(list).fromkeys(feat)
        categories = []
        median = []
        deviation = []
        data = []

        for key, value in feat.iteritems():

            texturefile = str(TEXTURE)
            temp[str(key)] = np.concatenate(value)
            element = [texturefile, key, value, temp[str(key)]]

            print "Texture file: ", texturefile
            print "Category: ", key
            categories.append(key)
            print "Median value: ", np.median(temp[str(key)])
            median.append(np.median(temp[str(key)]))
            print "Deviation: ", np.std(temp[str(key)])
            a = np.std(temp[str(key)])
            deviation.append((-a, a))

            data.append(temp[str(key)])

            print deviation
            myboxplot(texturefile, data, median, deviation, categories, DESTINATION_FOLDER)
