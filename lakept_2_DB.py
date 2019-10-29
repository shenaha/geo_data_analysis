## trying merging both geofabriks and geonames 
#import os
import csv
import time
import datetime
import MySQLdb
import pandas as pd 
import geopandas as gpd
from geopandas.tools import sjoin
from shapely.geometry import Point

start = time.time()
## read country file and get country,continent and geometry
countries = r"D:\data\final_files\Countries\ne_10m_admin_0_countries\ne_10m_admin_0_countries.shp"
out_file_shp = r"D:\data\final_files\Countries\ne_10m_admin_0_countries\Edited_country.shp"
countries_gdf  = gpd.read_file(countries)
countries_gdf.crs
countries_gdf1 = countries_gdf.rename(columns={'CONTINENT':'continent','NAME_EN':'country'})
countries_gdf2 = countries_gdf1[['country','continent','geometry']]

## Lake geonames 
geoLake_path = r"D:\data\final_files\Lake\Lake_geonames.csv"
pt_ed_lk = pd.read_csv(geoLake_path)
pt_ed_lk['modification_date'] = pt_ed_lk["modification_date"].apply(lambda v: datetime.datetime.strptime(v, '%Y-%m-%d'))
len(pt_ed_lk)
pt_ed_lk['name'].replace(['"', '#','/','1','2','3','4','5','6','`'], '')
## remove duplicates
pt_geo = pt_ed_lk.drop_duplicates(subset=None, inplace=False)
len(pt_geo)
## Lake geofabriks 
geofabLake_path = r"D:\data\final_files\Lake\Lake_geofabriks.csv"
pt_ed_lk1 = pd.read_csv(geofabLake_path)
pt_ed_lk1.insert(8,'modification_date','2019-03-27')
pt_ed_lk1['modification_date'] = pt_ed_lk1["modification_date"].apply(lambda v: datetime.datetime.strptime(v, '%Y-%m-%d'))
len(pt_ed_lk1)
pt_ed_lk1['name'].replace(['"', '#','/','1','2','3','4','5','6','`'], '')
## remove duplicates
pt_geoFab = pt_ed_lk1.drop_duplicates(subset=None, inplace=False)
len(pt_geoFab)
# merge geoname n geofab
combine_two_lk_pt = pd.concat([pt_geo,pt_geoFab],ignore_index = True)
len(combine_two_lk_pt)
pt1 = combine_two_lk_pt.drop_duplicates(subset=None, inplace=False)
len(pt1)
# find and replace 
findLak = ['H']
replaceLak = ['Hydro']
pt1['feature_class'] = pt1['feature_class'].replace(findLak,replaceLak)
#pt = pt1.rename(columns = {'name':'lake_name'}) 
#combine_two_lk_pt.to_csv(os.path.join(final_files,"Lakes.csv"), index=False)

## edit point files
pt1['latitude'] = pt1.latitude.apply(pd.to_numeric, args=('coerce',))
pt1['longitude'] = pt1.longitude.apply(pd.to_numeric, args=('coerce',))
pt1['geometry'] = pt1.apply(lambda z: Point(z.longitude, z.latitude), axis=1)
point_gdf = gpd.GeoDataFrame(pt1)
point_gdf.crs
point_gdf.crs = {'init': u'epsg:4326'}
point_gdf = point_gdf[point_gdf.is_valid == True]
## sjoin country and point file
merged_gdf = gpd.sjoin(point_gdf,countries_gdf2,how="right", op="within")
len(merged_gdf)
merged_gdf.head(10)
geoLake_out_Lake = r"D:\data\final_files\Lake\LakeFinal.csv"
merged_gdf_reorder = merged_gdf[['ID_source','name','feature_class','feature_code','latitude','longitude','country','continent','geometry','source','modification_date']]
merged_gdf_reorder.drop('geometry',axis=1).to_csv(geoLake_out_Lake,mode = 'w', index=False)
####
#geoLake_out_Lak1e = r"D:\data\final_files\Lake\LakeFinal222.csv"
#merged_gdf_reorder.to_csv(geoLake_out_Lak1e,mode = 'w', index=False)
#start = time.time()

## connect to a database
conn = MySQLdb.connect(host="localhost", port=3306, user="root", passwd="Pa$$w0rd", db="geonames", charset="utf8")
cur = conn.cursor()
cur.execute('DROP TABLE IF EXISTS lakePoints;')
## create table for lake points in Database
cur.execute("CREATE TABLE `geonames`.`lakePoints` ("
"`Lakept_ID` INT NOT NULL AUTO_INCREMENT,"
"`ID_source` INT NOT NULL,"
"`name` VARCHAR(100) NULL,"
"`feature_class` VARCHAR(20) NOT NULL,"
"`feature_code` VARCHAR(45) NOT NULL,"
"`latitude` DOUBLE NULL,"
"`longitude` DOUBLE NULL,"
"`country` VARCHAR(100) NOT NULL,"
"`continent` VARCHAR(100) NOT NULL,"
"`source` VARCHAR(45) NOT NULL,"
"`modification_date` DATE,"
"PRIMARY KEY (`Lakept_ID`));")


## read csv and insert into the database
with open(geoLake_out_Lake,encoding="utf8") as csvfile:
    reader = csv.DictReader(csvfile, delimiter = ',')
    for row in reader:
        print(row)
        #sql_statement = "INSERT IGNORE INTO points_lake(ID_source, lake_name, feature_class, feature_code, latitude, longitude, geometry) VALUES (%s, %s, %s, %s, %s, %s, ST_PointFromText(%s,0))"
        sql_statement = """INSERT INTO lakePoints(ID_source, name, feature_class, feature_code, latitude, longitude, country, continent, source, modification_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        cur = conn.cursor()
        param = [(row['ID_source'],row['name'],row['feature_class'],row['feature_code'],row['latitude'],row['longitude'],row['country'],row['continent'],row['source'],row['modification_date'])]
        cur.executemany(sql_statement,param)
        conn.escape_string(sql_statement)
        conn.commit()
    print("OVER")
    cur.close()
    conn.close()
    stop = time.time()
    elapsed = stop - start
    ## Pretty print elapsed
    if elapsed < 60:
        print("Lake points edited and inserted into the DB, it took {0:0.2f}s.".format(elapsed))
    elif elapsed < 3600:
        mins = int(elapsed/60)
        seconds = int(elapsed - 60*mins)
        print("Lake points edited and inserted into the DB, it took {}mins {}s.".format(mins, seconds))
    else:
        hours = int(elapsed/3600)
        mins = int((elapsed - 3600*hours) / 60)
        seconds = int(elapsed - 3600*hours - 60*mins)
        print("Lake points edited and inserted into the DB, it took {}hours {}mins {}s.".format(hours, mins, seconds))


import os, subprocess

base_path = "some/file/path"
loadfile = os.path.join(base_path, "file.xml")
command = ["C:/Program Files/QGIS 3.4/bin/ogr2ogr.exe","D:/script/hydro-CEM/output/62/countour.shp","D:/script/hydro-CEM/output/62/countour1.shp","-simplify","0.05"]
subprocess.check_call(command)

from osgeo import ogr
from shapely.geometry import Polygon
import fiona
x = fiona.open("D:/script/hydro-CEM/output/62/countour.shp")
poly = x.simplify(0.05, preserve_topology=True)
# Now convert it to a shapefile with OGR    
driver = ogr.GetDriverByName('Esri Shapefile')
ds = driver.CreateDataSource("D:/script/hydro-CEM/output/62/countour1.shp")
layer = ds.CreateLayer('', None, ogr.wkbPolygon)
# Add one attribute
layer.CreateField(ogr.FieldDefn('id', ogr.OFTInteger))
defn = layer.GetLayerDefn()
## If there are multiple geometries, put the "for" loop here
# Create a new feature (attribute and geometry)
feat = ogr.Feature(defn)
feat.SetField('id', 123)
# Make a geometry, from Shapely object
geom = ogr.CreateGeometryFromWkb(poly.wkb)
feat.SetGeometry(geom)
layer.CreateFeature(feat)
feat = geom = None  # destroy these
# Save and close everything
ds = layer = feat = geom = None