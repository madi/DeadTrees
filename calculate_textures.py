#!/usr/bin/env python

# calculate the PCA of the textures based on 4 bands orthophothos
# Author Margherita Di Leo
# Fri Jun  9 11:16:02 CEST 2017


from __future__ import print_function
import os,sys
import glob
import argparse
import grass.script as grass

#---function: parse input
def parseinput(name):
    '''Files contain "-" character that is not allowed
    in a name of a grass map. This function parses the input name and put "_"
    in place of "-"'''
    parsed = name.replace("-","_")
    return parsed

#---function: raster import
def rimport(INPUT_FOLDER, raster):
    '''Doesn't actually import, only registers
    '''
    parsed = parseinput(raster)
    cmd = 'r.external input=' + INPUT_FOLDER + raster + '.tif output=' + parsed
    os.system(cmd)

    # set working region
    cmd = 'g.region rast=' + parsed + '.4 -a'
    os.system(cmd)

    return parsed

#---function: export
def rexport(raster, DESTINATION_FOLDER):
    '''export to given destination folder'''
    outputpath = DESTINATION_FOLDER + raster + '.tif'
    cmd = 'r.out.gdal --o -f input=' + raster + ' output=' + outputpath
    print(cmd)
    os.system(cmd)


#---function: raster cleanup
def rcleanup(raster):
    '''delete raster files from grass mapset'''
    cmd = 'g.remove -f type=rast name=' + raster
    os.system(cmd)


#---function: calculate textures and PCA
def calculateTextures(ortho, DESTINATION_FOLDER):
    '''Calculates texures and PCA
    '''
    cmd = 'r.texture -a input=' + ortho + '.1 output=text_b1_' + ortho +' size=7 distance=5'
    os.system(cmd)
    cmd = 'r.texture -a input=' + ortho + '.4 output=text_b4_' + ortho +' size=7 distance=5'
    os.system(cmd)
    #cmd = 'i.group group=text_' + ortho + ' input=`g.list type=raster pattern=*text* mapset=. sep=,`'
    #os.system(cmd)
    #cmd = 'i.pca input=text_' + ortho + ' output=pca_text_' + ortho
    #os.system(cmd)
    #rexport('pca_text_' + ortho + '.1', DESTINATION_FOLDER)
    #rexport('pca_text_' + ortho + '.2', DESTINATION_FOLDER)

    textures = grass.read_command('g.list', type='raster', pattern='*text*', mapset='.', sep=',')
    textures = textures.split('\n')[0]
    lista = textures.split(',')
    for texture in lista:
        rexport(texture, DESTINATION_FOLDER)



#---MAIN
if __name__ == '__main__':

    ##---INPUT
    # parser
    parser = argparse.ArgumentParser(description = 'Calculate the PCA of the \
                                     textures based on 4 bands orthophothos')

    # path to input folder
    parser.add_argument('--infolder', dest = "infolder",
    help = "Folder where the input orthophothos are. ")

    # path to output folder
    parser.add_argument('--outfolder', dest = "outfolder",
    help = "Destination folder where the textures will be written.")

    args = parser.parse_args()

    global INPUT_FOLDER
    global DESTINATION_FOLDER

    INPUT_FOLDER = args.infolder
    DESTINATION_FOLDER = args.outfolder

    os.chdir(INPUT_FOLDER)

    tiles = []
    for file in glob.glob("*.tif") :
        tiles.append(file.split(".")[0])

    # set up GRASS environment
    GISBASE = os.environ['GISBASE'] = '/usr/local/grass-7.3.svn'
    GRASSDBASE = "/home/madi/grassdata"
    LOCATION = "Portugal"
    MAPSET = "batch_job"

    sys.path.append(os.path.join(os.environ['GISBASE'], "etc", "python"))
    import grass.script as grass
    import grass.script.setup as gsetup
    gsetup.init(GISBASE, GRASSDBASE, LOCATION, MAPSET)

    #---loop for all orthophothos in the input folder
    for tile in tiles :

        print("Importing : ", tile)
        ortho = rimport(INPUT_FOLDER, tile)
        calculateTextures(ortho, DESTINATION_FOLDER)
        # cleanup all
        #cmd = 'g.remove -f type=rast pattern=*' + ortho + '*'
        #os.system(cmd)

    print("Done the job!")
