#---------------------------------------------------------------------------------------------------------#
#             Script to merge lake and river .csv files from both geonames and geofabriks                 #
#---------------------------------------------------------------------------------------------------------#
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
'''
Inspired from vitalis https://www.quora.com/In-Python-3-how-do-I-merge-thousands-of-CSV-files-remove-records-with-blanks-and-write-to-one-CSV-efficiently-without-consuming-huge-memory

'''
#------------------------------------------#
#          Merge Geonames files            #
#------------------------------------------#
output_lake_geo = "D:/data/final_files/Lake/Lake_geonames.csv"
output_riv_geo = "D:/data/final_files/River/River_geonames.csv"
unzipFileGeoPath = "D:/data/geonames/extracted"

first_file=True
for root, dirs, files in os.walk(unzipFileGeoPath):
    for file in files:
        if file.startswith("River"):
            rivPath = os.path.join(root, file)
            rivPath
            df_Riv = pd.read_csv(rivPath)
            ## inspired from https://stackoverflow.com/a/35970219
            header=['ID_source', 'name','feature_code','feature_class','latitude','longitude','geometry','source','modification_date']
            #df_Riv.drop_duplicates(subset=None, inplace=True)
            if first_file:
                df_Riv.to_csv(output_riv_geo,index=False)
                first_file = False
            else:
                df_Riv.to_csv(output_riv_geo,index=False, header=header, mode='a')
                print("River complete....")
            #
        elif file.startswith("Lake"):
            lakePath = os.path.join(root, file)
            lakePath
            df_Lake = pd.read_csv(lakePath)
            if first_file:
                df_Lake.to_csv(output_lake_geo,index=False)
                first_file = False
            else:
                df_Lake.to_csv(output_lake_geo,index=False, header=False, mode='a')
            print("Lake complete, moving to river....")
        ##
        stop = time.time()
        elapsed = stop - start
        # Pretty print the time elapsed
        if elapsed < 60:
            print("Merging CSVs finished, it took {0:0.2f}s.".format(elapsed))
        elif elapsed < 3600:
            mins = int(elapsed/60)
            seconds = int(elapsed - 60*mins)
            print("Merging CSVs finished, it took {}mins {}s.".format(mins, seconds))
        else:
            hours = int(elapsed/3600)
            mins = int((elapsed - 3600*hours) / 60)
            seconds = int(elapsed - 3600*hours - 60*mins)
            print("Merging CSVs finished, it took {}hours {}mins {}s.".format(hours, mins, seconds))


#------------------------------------------#
#          Merge Geofabrik files           #
#------------------------------------------#

start = time.time()
output_lake_geoFab = 'D:/data//final_files/Lake/Lake_geofabriks.csv'
output_riv_geoFab = 'D:/data/final_files/River/River_geofabriks.csv'
unzipFilePath = "D:/data/geofabrik/extracted"
first_file=True
for root, dirs, files in os.walk(unzipFilePath):
    for file in files:
        if file.endswith("FinalLake.csv"):
            lakePath = os.path.join(root, file)
            df_Lake_gf = pd.read_csv(lakePath)
            #df_Lake_gf.drop_duplicates(subset=None, inplace=True)
            if first_file:
                df_Lake_gf.to_csv(output_lake_geoFab,index=False)
                first_file = False
            else:
                df_Lake_gf.to_csv(output_lake_geoFab,index=False, header=False, mode='a')
                print("Lake complete, moving to river....")
        elif file.endswith("FinalRiver.csv"):
            rivPath = os.path.join(root, file)
            df_Riv_gf = pd.read_csv(rivPath)
            #df_Riv_gf.drop_duplicates(subset=None, inplace=True)
            if first_file:
                df_Riv_gf.to_csv(output_riv_geoFab,index=False)
                first_file = False
            else:
                df_Riv_gf.to_csv(output_riv_geoFab,index=False, header=False, mode='a')
                print("River complete....")
'''              
for root, dirs, files in os.walk(root1):
    for file in files:
        if file.endswith("FinalRiver.csv"):
            rivPath = os.path.join(root, file)
            rivPath
            df_Riv_gf = pd.read_csv(rivPath)
            #df_Riv_gf.drop_duplicates(subset=None, inplace=True)
            if first_file:
                df_Riv_gf.to_csv(output_riv_geoFab,index=False)
                first_file = False
            else:
                df_Riv_gf.to_csv(output_riv_geoFab,index=False, mode='a')
                print("River complete....")
''' 
stop = time.time()
elapsed = stop - start
    # Pretty print the time elapsed
if elapsed < 60:
    print("Process finished, it took {0:0.2f}s.".format(elapsed))
elif elapsed < 3600:
    mins = int(elapsed/60)
    seconds = int(elapsed - 60*mins)
    print("Process finished, it took {}mins {}s.".format(mins, seconds))
else:
    hours = int(elapsed/3600)
    mins = int((elapsed - 3600*hours) / 60)
    seconds = int(elapsed - 3600*hours - 60*mins)
    print("Process finished, it took {}hours {}mins {}s.".format(hours, mins, seconds))
