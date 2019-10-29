#--------------------------------------------------------------------------------------------------#
#                       Script to extract lakes and rivers from GEONAMES                           #
#--------------------------------------------------------------------------------------------------#
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

#---------------------------#
#      Lake function        #
#---------------------------#
'''
lakeIn  - Input file  = geonamesfinalPath 
          formate = textfile
lakeOut - Output file = lake_feature
          formate = CSV file

'lakeIn' file is separated into columns based on http://download.geonames.org/export/dump/readme.txt 
'lake_list' & 'lake_list1' contains code from  https://www.geonames.org/export/codes.html

'''

def Lake_geo(lakeIn,lakeOut):
    ## Read .txt file and separate into columns
    data = pd.read_csv(lakeIn, sep="\t", header=None)
    data.columns = ["geonameid", "name", "asciiname", "alternatenames", "latitude","longitude", "feature_class", "feature_code", "country", "cc2","admin1_code1", "admin2_code", "admin3_code", "admin4_code","population", "elevation", "dem", "timezone", "modification_date"]
    list_columns = ["name","alternatenames", "country", "cc2","admin1_code1", "admin2_code", "admin3_code", "admin4_code","population", "elevation", "dem", "timezone"]
    r = data.drop(list_columns,axis=1)  ## drop columns
    ## Grouping based on feature_class Hydro
    hydro = r.loc[r["feature_class"] == 'H']
    ## Check if the feature_code listed are within hydro
    lake_list = ['RSV','RSVI','PND','PNDI','PNDN','PNDNI','PNDS','PNDSF','PNDSI','PNDSN','WTRH','MRSH','MRSHN','SPNG','SPNT','SPNS']
    lake_col = hydro[hydro["feature_code"].isin(lake_list)]
    r1 = lake_col.rename(columns = {'geonameid':'ID_source','asciiname':'name'})     ## renaming columns
    lake_list1 = ['LK','LKI','LKS','LKSI','LKN','LKNI','LKSN','LKSNI','LKO','LKSC','LKX']
    lake_col_1 = hydro[hydro["feature_code"].isin(lake_list1)]   # isin function
    r2 = lake_col_1.rename(columns = {'geonameid':'ID_source','asciiname':'name'})   ## renaming columns
    ## combine files r1 and r2
    df = pd.concat([r1,r2],ignore_index = True)
    df.insert(6,'source','www.geonames.org') ## insert columns
    #geometry_lak = [Point(xy) for xy in zip(df['longitude'], df['latitude'])]
    #df.insert(5,'geometry',geometry_lak)
    #
    r_reorder1 = df[['ID_source', 'name', 'feature_class','feature_code','latitude','longitude','source','modification_date']] # rearrange column here
    ## find and replace codes with its abbreviation 
    findL = ['LK','LKI','LKS','LKSI','LKN','LKNI','LKSN','LKSNI','LKO','LKOI','LKSC','LKX','RSV','RSVI','PND','PNDI','PNDN','PNDNI','PNDS','PNDSF','PNDSI','PNDSN','WTRH','MRSH','MRSHN','SPNG']
    replaceL = ['Lake','intermittent_lake','Lakes','intermittent_lakes','salt_lake','intermit_salt_lake','salt_lakes','intermittent_salt_lakes','oxbow_lake','intermittent_oxbow_lake','crater_lakes','section_of_lake','reservoirs','intermittent_reservoir','pond','intermittent_pond','salt_pond','intermittent_salt_ponds','ponds','fishponds','intermittent_ponds','salt_ponds','waterholes','marshes','salt_marshes','spring']
    r_reorder1['feature_code'] = r_reorder1['feature_code'].replace(findL,replaceL)
    r_reorder1.to_csv(lakeOut,mode = 'w', index=False)  ## Writing output as CSV

#-----------------------------#
#       River function        #
#-----------------------------#
'''
riverIn  - Input file  = geonamesfinalPath 
          formate = textfile
riverOut - Output file = lake_feature
          formate = CSV file

'riverIn' file is separated into columns based on http://download.geonames.org/export/dump/readme.txt 
'river_list' contains code from  https://www.geonames.org/export/codes.html

'''

def River_geo(riverIn,riverOut):
    ## Read .txt file and separate into columns
    data1 = pd.read_csv(riverIn, sep="\t", header=None)
    data1.columns = ["geonameid", "name", "asciiname", "alternatenames", "latitude","longitude", "feature_class", "feature_code", "country", "cc2","admin1_code1", "admin2_code", "admin3_code", "admin4_code","population", "elevation", "dem", "timezone", "modification_date"]
    list_columns1 = ["name","alternatenames","country","cc2","admin1_code1", "admin2_code", "admin3_code", "admin4_code","population", "elevation", "dem", "timezone"]
    r1 = data1.drop(list_columns1,axis=1)  ## drop unwanted columns
    ## Grouping based on feature_class Hydro
    hydro1 = r1.loc[r1["feature_class"] == 'H']
    ## Check if the feature_code listed are within hydro
    river_list = ['STM','STMS','STMD','STMI','STMX','STMIX','STMM','SWMP','WTRC']
    river_col = hydro1[hydro1["feature_code"].isin(river_list)]  # isin function
    riv = river_col.rename(columns = {'geonameid':'ID_source','asciiname':'name'}) ## renaming columns
    riv.insert(6,'source','www.geonames.org')
    #geometry_riv = [Point(xy) for xy in zip(riv['longitude'], riv['latitude'])]
    #riv.insert(5,'geometry',geometry_riv)
    #
    ## find and replace codes with its abbreviation 
    r_reorder = riv[['ID_source', 'name','feature_code','feature_class','latitude','longitude','source','modification_date']] # rearrange column here
    findR = ['STM','STMS','STMD','STMI','STMX' ,'STMIX','STMM','SWMP','WTRC']
    replaceR = ['stream','streams','distributary','intermittent_stream','section_of_stream','section_of_intermittent_stream','stream_mouths','swamp','watercourse']
    ## reorder
    r_reorder['feature_code'] = r_reorder['feature_code'].replace(findR,replaceR)
    r_reorder.to_csv(riverOut,mode = 'w', index=False,header=True) ## Writing output as CSV

#---------------------------------------------------------------------#
#              Main calling the Lake and River functions              #
#---------------------------------------------------------------------#

start = time.time()
unzipFileGeoPath = "D:/data/geonames/extracted"
for root, dirs, files in os.walk(unzipFileGeoPath):
    for file in files:
        if file.endswith(".txt"):
            geonamesfinalPath = os.path.join(root, file)
            print(geonamesfinalPath)
            lake_feature = os.path.join(root,"Lake.csv")
            river_features = os.path.join(root,"River.csv")
            ## function calling 
            Lake_geo(geonamesfinalPath,lake_feature)
            River_geo(geonamesfinalPath,river_features)
            print("Finished.... "+os.path.join(root, file)+" moving on to the next file....") 
            stop = time.time()
            elapsed = stop - start
            # Pretty print the time elapsed
            if elapsed < 60:
                print("Lake and River separation process finished for "+os.path.splitext(file)[0]+" took {0:0.2f}s.".format(elapsed))
            elif elapsed < 3600:
                mins = int(elapsed/60)
                seconds = int(elapsed - 60*mins)
                print("Lake and River separation process finished for "+os.path.splitext(file)[0]+" took {}mins {}s.".format(mins, seconds))
            else:
                hours = int(elapsed/3600)
                mins = int((elapsed - 3600*hours) / 60)
                seconds = int(elapsed - 3600*hours - 60*mins)
                print("Lake and River separation for "+os.path.splitext(file)[0]+" took {}hours {}mins {}s.".format(hours, mins, seconds))


#-----------------------------------------------#
#              remove 1kb files                 #
#-----------------------------------------------#
start = time.time()
unzipFileGeoPath = "D:/data/geonames/extracted"
for root, dirs, files in os.walk(unzipFileGeoPath):
    for file in files:
        if file.endswith(".csv"):
            lakePath = os.path.join(root, file)
            #lakePath
            if os.path.getsize(lakePath) < 1024:
                os.remove(lakePath)
            elif os.path.getsize(lakePath) < 0:
                os.remove(lakePath)
            else:
                print("No such files found !!")
