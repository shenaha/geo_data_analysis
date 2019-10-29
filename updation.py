import time
import os,sys
import urllib
import pandas as pd
import urllib.request
from tqdm import tqdm
import zipfile,fnmatch
import zipfile,fnmatch
from shapely.geometry import Point
import geopandas as gpd
from geopandas import GeoDataFrame


old = r"D:\data\geonames\try\extractedOld\CA\Lake.csv"
new = r"D:\data\geonames\try\extractedNew\CA\Lake.csv"
updated = r"D:\data\geonames\try\diff."

for root, dirs, files in os.walk(old):
    for file in files:
        if file.endswith(".csv"):
            d = os.path.join(root, file)
            print(d)

# Inspired from https://stackoverflow.com/a/38996374/11293041
## read old and new files , find the difference 
with open(old, 'r') as t1, open(new, 'r') as t2:
    fileone = t1.readlines()
    filetwo = t2.readlines()

## write the diff values to a  new file
with open(updated, 'w',header='header') as outFile:
    for line in filetwo:
        if line not in fileone:
            outFile.write(line)

## updated file 
read_newFiles = pd.read_csv(updated)
read_newFiles.head(4)
header=['ID_source', 'name','feature_code','feature_class','latitude','longitude','geometry','source','modification_date']
read_newFiles.to_csv(updated,index=False, header=header) ## override new files with header
## old files
read_oldFiles = pd.read_csv(old)
read_oldFiles.head(4)
read_oldFiles = read_oldFiles[['ID_source', 'name', 'feature_class','feature_code','latitude','longitude','geometry','source']] ## rearrange column here
read_oldFiles.insert(9,'status','Old')
## updated file
read_newFiles= pd.read_csv(updated)
read_newFiles.head(4)
read_newFiles = read_newFiles[['ID_source', 'name', 'feature_class','feature_code','latitude','longitude','geometry','source']] ## rearrange column here
read_newFiles.insert(9,'status','Updated')
## append the rows of new files with old
out = read_oldFiles.append(read_newFiles)
out.to_csv(old,index=False) ## overwrite in the old files