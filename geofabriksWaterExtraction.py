#--------------------------------------------------------------------------------------------------#
#                       Script to extract lakes and rivers from GEOFABRIKS                         #
#--------------------------------------------------------------------------------------------------#
import os
import time
import fiona
import datetime
import pandas as pd
from tqdm import tqdm
import zipfile,fnmatch
import geopandas as gpd
from shapely.geometry import shape, mapping

zipfilePath = "D:/data/geofabrik/zipfiles"
unzipFilePath = "D:/data/geofabrik/extracted"

#---------------------------#
#      Lake function        #
#---------------------------#
'''
infileLake     - Input file (.shp)
outfileLake    - Output centroid file (.shp)
out_file_Lake  - Contain nameEdited file (.shp)
afileLake      - Contain X,Y,geometry (.csv)
bfileLake      - Contain name,feature class (.csv)
finalLake      - Contains values of both 'afileLake' & 'bfileLake'
endLake        - Final edited lake file (.csv)

modification_date = will contain the date when the script is processed
                    if that is not needed then do as below : 
                         around Line 81-83 :
                              #dateCurr = pd.to_datetime('today').strftime("%Y-%m-%d")
                              #Lrenamed.insert(7,'modification_date',dateCurr)
                              Lrenamed.insert(7,'modification_date','2019-03-29') ## manually enter the date you want

'''

def Lake(infileLake,outfileLake,out_file_Lake,afileLake,bfileLake,finalLake,endLake):
    start = time.time()
    ## find centroid and convert to a CSV file 
    with fiona.open(infileLake) as input:
        # change only the geometry of the schema: LineString -> Point
        input.schema['geometry'] = "Point"
        # write the Point shapefile
        with fiona.open(outfileLake, 'w','ESRI Shapefile', input.schema.copy(), input.crs, encoding='utf-8') as output:
            for elem in input:
                # GeoJSON to shapely geometry
                geom = shape(elem['geometry'])
                # shapely centroid to GeoJSON
                elem['geometry'] = mapping(geom.centroid)
                output.write(elem)
    #---------------------------------------------------------------------------   
    shp = gpd.read_file(outfileLake)
    shp["X"] = shp["geometry"].apply(lambda geom: geom.y)
    shp["Y"] = shp["geometry"].apply(lambda geom: geom.x)
    shp["geometry"] = shp["geometry"]
    shp[["X","Y","geometry"]].to_csv(afileLake,header=True,index=False,sep=",")
    # delete no name column
    selection = shp.loc[shp['name'] !='']
    selection.head(4)
    selection.to_file(out_file_Lake)
    #--------------------------------------------------------------------------##
    shp1 = gpd.read_file(out_file_Lake)
    title_col = shp1.columns[0]
    name_map = dict(zip(shp1.columns[[0,3]], ['osmid', 'name','fclass']))
    shp1.rename(columns=name_map, inplace=True)
    # rename column
    findName = ['water']
    replaceName = ['lake']
    shp1['fclass'] = shp1['fclass'].replace(findName,replaceName)
    shp1[['osmid', 'name','fclass','geometry']].to_csv(bfileLake,header=True,index=False,sep=",") 
    a = pd.read_csv(afileLake)
    b = pd.read_csv(bfileLake)
    # combine two files
    merged = pd.merge(b,a,on='geometry',how='inner')
    merged.to_csv(finalLake, index=False)
    ##------------------------------------------------------------------------##
    ### with pandas rename,insert,remove duplicate,reorder columns and save it as CSV
    fileDataEditLake = pd.read_csv(finalLake,index_col=None, header=0)
    Lrenamed = fileDataEditLake.rename(columns = {'osmid':'ID_source','fclass':'feature_code','X':'latitude','Y':'longitude'}) # rename
    # add columns
    Lrenamed.insert(3,'feature_class','Hydro')
    dateCurr = pd.to_datetime('today').strftime("%Y-%m-%d")
    Lrenamed.insert(6,'source','www.geofabrik.de')
    Lrenamed.insert(7,'modification_date',dateCurr)
    Lrenamed['modification_date'] = Lrenamed["modification_date"].apply(lambda v: datetime.datetime.strptime(v, '%Y-%m-%d')) ## change datatype to DATE
    Lreorder = Lrenamed[['ID_source', 'name', 'feature_class','feature_code','latitude','longitude','geometry','source']] ## rearrange column here
    Lreorder.to_csv(endLake,mode = 'w', index=False,encoding='utf-8-sig')
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


#-----------------------------#
#       River function        #
#-----------------------------#
'''
infileRiver    - Input file (.txt)
outfileRiver   - Output centroid file (.csv)
out_file_River - Contain X,Y,geometry (.csv)
afileRiver     - Contain name,feature class (.csv)
bfileRiver     - Contains values of both 'afileLake' & 'bfileLake'
endRiver       - Final edited lake file (.csv)

modification_date = will contain the date when the script is processed
                    if that is not needed then do as below : 
                         around Line 81-83 :
                              #dateCurr = pd.to_datetime('today').strftime("%Y-%m-%d")
                              #Lrenamed.insert(7,'modification_date',dateCurr)
                              Lrenamed.insert(7,'modification_date','2019-03-29') ## manually enter the date you want

'''

def River(infileRiver,outfileRiver,out_file_River,afileRiver,bfileRiver,finalRiver,endRiver):
    start=time.time()
    ## find centroid and convert to a CSV file 
    with fiona.open(infileRiver) as input:
        # change only the geometry of the schema: LineString -> Point
        input.schema['geometry'] = "Point"
        # write the Point shapefile
        with fiona.open(outfileRiver, 'w', 'ESRI Shapefile', input.schema.copy(), input.crs, encoding='utf-8') as output:
            for elemR in input:
                # GeoJSON to shapely geometry
                geom = shape(elemR['geometry'])
                # shapely centroid to GeoJSON
                elemR['geometry'] = mapping(geom.centroid)
                output.write(elemR)
    #---------------------------------------------------------------------------------------------------#
    shpR = gpd.read_file(outfileRiver)
    shpR["X"] = shpR["geometry"].apply(lambda geom: geom.y)
    shpR["Y"] = shpR["geometry"].apply(lambda geom: geom.x)
    shpR["geometry"] = shpR["geometry"]
    shpR[["X","Y","geometry"]].to_csv(afileRiver,header=True,index=False,sep=",")
    ### delete no name column
    selectionR = shpR.loc[shpR["name"] !=""]
    selectionR.to_file(out_file_River)
    #---------------------------------------------------------------------------------------------------#
    shp1R = gpd.read_file(out_file_River)
    #shp1R = gpd.read_file(r"D:\data\geofabrik\extracted\Africa\algeria-latest-free.shp\nameEditedRiver.shp")
    #drop_col = ['width']
    #shp1R = shp1R.drop(drop_col,axis=1)
    title_colR = shp1R.columns[0]
    name_map = dict(zip(shp1R.columns[[0,4]], ['osmid', 'name','fclass']))
    shp1R.rename(columns=name_map, inplace=True)
    shp1R[['osmid', 'name','fclass','geometry']].to_csv(bfileRiver,header=True,index=False,sep=",") 
    aR = pd.read_csv(afileRiver)
    bR = pd.read_csv(bfileRiver)
    # combine two files
    mergedR = pd.merge(bR,aR,on='geometry',how='inner')
    mergedR.to_csv(finalRiver, index=False)
    ##-------------------------------------------------------------------------------------------------#
    ### with pandas rename,insert,remove duplicate,reorder columns and save it as CSV
    fileDataEditRiver = pd.read_csv(finalRiver,index_col=None, header=0)
    #fileDataEditRiver = pd.read_csv(r"D:\data\geofabrik\extracted\Africa\algeria-latest-free.shp\endCSVRiver.csv",index_col=None, header=0)
    Rrenamed = fileDataEditRiver.rename(columns = {'osmid':'ID_source','fclass':'feature_code','X':'latitude','Y':'longitude'})
    # add columns
    Rrenamed.insert(3,'feature_class','Hydro')
    dateCurr = pd.to_datetime('today').strftime("%Y-%m-%d")
    Rrenamed.insert(6,'source','www.geofabrik.de')
    Rrenamed.insert(7,'modification_date',dateCurr)
    Rrenamed['modification_date'] = Rrenamed["modification_date"].apply(lambda v: datetime.datetime.strptime(v, '%Y-%m-%d'))
    Rreorder = Rrenamed[['ID_source', 'name', 'feature_class','feature_code','latitude','longitude','geometry','source']] # rearrange column here
    Rreorder.to_csv(endRiver,mode = 'w', index=False,encoding='utf-8-sig')
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


#---------------------------------------------------------------------#
#              Main calling the Lake and River functions              #
#---------------------------------------------------------------------# 

start = time.time()
for root, dirs, files in os.walk(unzipFilePath):
    for file in files:
        if file.endswith("gis_osm_waterways_free_1.shp"):
            finalPath1 = os.path.join(root, file)
            print(finalPath1)
            infileRiver = finalPath1
            outfileRiver = os.path.join(root,"outRiver.shp")
            out_file_River = os.path.join(root,"nameEditedRiver.shp")
            afileRiver = os.path.join(root,"coordsRiver.csv")
            bfileRiver = os.path.join(root,"extractedTableRiver.csv")
            finalRiver = os.path.join(root,"endCSVRiver.csv")
            endRiver = os.path.join(root,"editedFinalRiver.csv")
            #print(outfile,out_file,afile,bfile,final)
            ## calling River function 
            River(infileRiver,outfileRiver,out_file_River,afileRiver,bfileRiver,finalRiver,endRiver)
            print("river process ended...successful")
        elif file.endswith("gis_osm_water_a_free_1.shp"):
            finalPath = os.path.join(root, file)
            infileLake = finalPath
            print(infileLake)
            outfileLake = os.path.join(root,"outLake.shp")
            out_file_Lake = os.path.join(root,"nameEditedLake.shp")
            afileLake = os.path.join(root,"coordsLake.csv")
            bfileLake = os.path.join(root,"extractedTableLake.csv")
            finalLake = os.path.join(root,"endCSVLake.csv")
            endLake = os.path.join(root,"editedFinalLake.csv")
            #print(outfileLake,out_file_Lake,afileLake,bfileLake,finalLake)
            ## calling Lake function 
            Lake(infileLake,outfileLake,out_file_Lake,afileLake,bfileLake,finalLake,endLake)
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


#-----------------------------------------#
#              remove files               #
#-----------------------------------------#
'''
removing all the intermediate file generated during the above process

'''
for root, dirs, files in os.walk(unzipFilePath):
    for file in files:
        if file.startswith("nameEdited"):
            nameEdited = os.path.join(root, file)
            os.remove(nameEdited)
            print("Remove file starting with nameEdited")
        elif file.startswith("out"):
            out = os.path.join(root, file)
            os.remove(out)
            print("Remove file starting with out")
        elif file.startswith("endCSV"):
            editedFinal = os.path.join(root, file)
            os.remove(editedFinal)
            print("Remove file starting with endCSV")
