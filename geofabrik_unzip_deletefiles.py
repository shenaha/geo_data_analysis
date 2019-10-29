#--------------------------------------------------------------------------------------------------#
#                      Script to unzip and extract files from GEOFABRIK                            #
#--------------------------------------------------------------------------------------------------#
import os
import time
import fiona
import pandas as pd
from tqdm import tqdm
import zipfile,fnmatch
import geopandas as gpd
from shapely.geometry import shape, mapping
from geonames_unzip_deletefiles import fileExits

#------------------------------------------------#
#              Unzipping .zip files              #
#------------------------------------------------#
'''
zipfilePath     - path to the folder containing the .zip files
                  change this path based on the location of the geofabrik .zip files

unzipFilePath   - path to the folder containing the extracted files
                  change this path folder based on the location of where you want to extract your files

'''
start = time.time()
zipfilePath = "D:/data/geofabrik/zipfiles"
unzipFilePath = "D:/data/geofabrik/extracted"
fileExits(zipfilePath)
fileExits(unzipFilePath)
pattern = '*.zip'
## looping to read all the .zip files in the 'zipfilePath' folder
for root, dirs, files in os.walk(zipfilePath):
    for filename in fnmatch.filter(files, pattern):
        geofab_zip_paths = os.path.join(root, filename)
        print(geofab_zip_paths)
        head,tail = os.path.split(geofab_zip_paths)
        folder_name = os.path.basename(head)
        ## unzipping
        zipfile.ZipFile(geofab_zip_paths).extractall(os.path.join(unzipFilePath,folder_name,os.path.splitext(filename)[0]))
        stop = time.time()
        elapsed = stop - start
        # Pretty print the time elapsed
        if elapsed < 60:
            print("Process finished, it took {0:0.2f}s. to unzip".format(elapsed))
        elif elapsed < 3600:
            mins = int(elapsed/60)
            seconds = int(elapsed - 60*mins)
            print("Process finished, it took {}mins {}s. to unzip".format(mins, seconds))
        else:
            hours = int(elapsed/3600)
            mins = int((elapsed - 3600*hours) / 60)
            seconds = int(elapsed - 3600*hours - 60*mins)
            print("Process finished, it took {}hours {}mins {}s. to unzip".format(hours, mins, seconds))

#------------------------------------------------#
#          Delete unimportant files              #
#------------------------------------------------#
'''
Delete other unimportant files not starting with "gis_osm_water" from the folder 'unzipFilePath'

water_file      - file list containing 'gis_osm_water' file paths
non_waterFile   - file list containing other unimportant file paths

'''
# looping to remove all the unimportant files in the 'unzipFilePath' folder
for root, dirs, files in os.walk(unzipFilePath):
     for file in files:
        if file.startswith("gis_osm_water"):
            water_file = os.path.join(root, file)
            #print(water_file)
        else:
            non_waterFile = os.path.join(root, file)
            print(non_waterFile)
            print("Unimportant files going to be Removed...")
            os.remove(non_waterFile)
            print("Deleted unimportant files...")