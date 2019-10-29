#---------------------------------------------------------------------#
#                        River point database                         #
#---------------------------------------------------------------------#
import os
import csv
import time
import MySQLdb
import datetime
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

## River geonames
geoRiver_path = r"D:\data\final_files\River\River_geonames.csv"
pt_ed_riv = pd.read_csv(geoRiver_path)
pt_ed_riv['modification_date'] = pt_ed_riv["modification_date"].apply(lambda v: datetime.datetime.strptime(v, '%Y-%m-%d'))
pt_ed_riv.head(5)
len(pt_ed_riv)
pt_ed_riv['name'].replace(['"', '#','/','1','2','3','4','5','6','`'], '')
## remove duplicates
pt_geo_riv = pt_ed_riv.drop_duplicates(subset=None, inplace=False)
len(pt_geo_riv)
#
## River geofabriks
'''
geofabRiver_path = r"D:\data\final_files\River\River_geofabriks.csv"
pt_ed_riv1 = pd.read_csv(geofabRiver_path)
pt_ed_riv1.insert(9,'modification_date','2019-03-27')
pt_ed_riv1['modification_date'] = pt_ed_riv1["modification_date"].apply(lambda v: datetime.datetime.strptime(v, '%Y-%m-%d'))
len(pt_ed_riv1)
## remove duplicates
pt_geoFab_riv = pt_ed_riv1.drop_duplicates(subset=None, inplace=False)
len(pt_geoFab_riv)
# merge geoname n geofab
combine_two_riv_pt = pd.concat([pt_geo_riv,pt_geoFab_riv],ignore_index = True)
len(combine_two_riv_pt)
pt_riv1 = combine_two_riv_pt.drop_duplicates(subset=None, inplace=False)
len(pt_riv1)
'''
# find and replace 
findRi = ['H']
replaceRi = ['Hydro']
pt_geo_riv['feature_class'] = pt_geo_riv['feature_class'].replace(findRi,replaceRi)
#pt_geo_riv = pt_geo_riv.rename(columns = {'name':'lake_name'}) 

## edit point files
pt_geo_riv['latitude'] = pt_geo_riv.latitude.apply(pd.to_numeric, args=('coerce',))
pt_geo_riv['longitude'] = pt_geo_riv.longitude.apply(pd.to_numeric, args=('coerce',))
pt_geo_riv['geometry'] = pt_geo_riv.apply(lambda z: Point(z.longitude, z.latitude), axis=1)
point_gdf_riv = gpd.GeoDataFrame(pt_geo_riv)
point_gdf_riv.crs
point_gdf_riv.crs = {'init': u'epsg:4326'}
point_gdf_riv = point_gdf_riv[point_gdf_riv.is_valid == True]
## sjoin country and point file
merged_gdf_ri = gpd.sjoin(point_gdf_riv,countries_gdf2,how="right", op="within")
len(merged_gdf_ri)
merged_gdf_ri.head(10)
geoRiver_out_River = r"D:\data\final_files\River\RiverFinal.csv"
merged_gdf_reorder_ri = merged_gdf_ri[['ID_source','name','feature_class','feature_code','latitude','longitude','country','continent','geometry','source','modification_date']]
merged_gdf_reorder_ri.drop('geometry',axis=1).to_csv(geoRiver_out_River,mode = 'w', index=False)

## connect to a database
conn = MySQLdb.connect(host="localhost", port=3306, user="root", passwd="Pa$$w0rd", db="geonames", charset="utf8")
cur = conn.cursor()
cur.execute('DROP TABLE IF EXISTS riverPoints;')
## create table for river points in Database
cur.execute("CREATE TABLE `geonames`.`riverPoints` ("
"`Riverpt_ID` INT NOT NULL AUTO_INCREMENT,"
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
"PRIMARY KEY (`Riverpt_ID`));")


## read csv and insert into the database
with open(geoRiver_out_River,encoding="utf8") as csvfile:
    reader = csv.DictReader(csvfile, delimiter = ',')
    for row in reader:
        print(row)
        #sql_statement = "INSERT IGNORE INTO points_lake(ID_source, lake_name, feature_class, feature_code, latitude, longitude, geometry) VALUES (%s, %s, %s, %s, %s, %s, ST_PointFromText(%s,0))"
        sql_statement = """INSERT INTO riverPoints(ID_source, name, feature_class, feature_code, latitude, longitude, country, continent, source, modification_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
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
        print("River points edited and inserted into the DB, it took {0:0.2f}s.".format(elapsed))
    elif elapsed < 3600:
        mins = int(elapsed/60)
        seconds = int(elapsed - 60*mins)
        print("River points edited and inserted into the DB, it took {}mins {}s.".format(mins, seconds))
    else:
        hours = int(elapsed/3600)
        mins = int((elapsed - 3600*hours) / 60)
        seconds = int(elapsed - 3600*hours - 60*mins)
        print("River points edited and inserted into the DB, it took {}hours {}mins {}s.".format(hours, mins, seconds))
