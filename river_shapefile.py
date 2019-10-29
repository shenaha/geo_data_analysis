#----------------------------------------------------------------------------------------------#
#                       Create River database and insert values                                #
#----------------------------------------------------------------------------------------------#

import os
import csv
import sys
import time
import MySQLdb
import gdal,ogr
import shapefile
import pandas as pd
import geopandas as gp
from geopandas.tools import sjoin
from shapely.geometry import Polygon, MultiPolygon, shape, Point

## inspired from https://stackoverflow.com/a/15063941
## error was "_csv.Error: field larger than field limit (131072)"
## increase the size of csv 
maxInt = sys.maxsize

while True:
    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt = int(maxInt/10)


def convert_3D_2D(geometry):
    '''
    Converts 3D geometry of the lakes to 2D
    Takes a GeoSeries of Multi/Polygons and returns a list of Multi/Polygons
    '''
    import geopandas as gp
    new_geo = []
    for p in geometry:
        if p.has_z:
            if p.geom_type == 'Polygon':
                lines = [xy[:2] for xy in list(p.exterior.coords)]
                new_p = Polygon(lines)
                new_geo.append(new_p)
            elif p.geom_type == 'MultiPolygon':
                new_multi_p = []
                for ap in p:
                    lines = [xy[:2] for xy in list(ap.exterior.coords)]
                    new_p = Polygon(lines)
                    new_multi_p.append(new_p)
                new_geo.append(MultiPolygon(new_multi_p))
    return new_geo


start = time.time()
## connect to Database
conn = MySQLdb.connect(host="localhost", port=3306, user="root", passwd="Pa$$w0rd", db="geonames", charset="utf8")
cur = conn.cursor()
cur.execute('DROP TABLE IF EXISTS riverShp;')
## create table for river shapefile in Database
cur.execute("CREATE TABLE `geonames`.`riverShp` ("
 "`RiverID` INT NOT NULL AUTO_INCREMENT,"
  "`Z_min_m` FLOAT NULL,"
  "`Z_max_m` FLOAT NULL,"
  "`Perimeter_m` FLOAT NULL,"
  "`Area_km2` FLOAT NULL,"
  "`X_Center` DOUBLE NULL,"
  "`Y_Center` DOUBLE NULL,"
  "`Xmin` DOUBLE NULL,"
  "`Xmax` DOUBLE NULL,"
  "`Ymin` DOUBLE NULL,"
  "`Ymax` DOUBLE NULL,"
  "`geometry` POLYGON NOT NULL,"
  "PRIMARY KEY (`RiverID`));")

output_path = r'D:\script\hydro-CEM\output'
for root, dirs, files in os.walk(output_path):
  for file in files:
    if file.startswith("rivers.shp"):
      river_shp_whl = os.path.join(root, file)
      print(river_shp_whl)
      pathEditedRivers = os.path.join(root,"edited_river.csv")
      dfR = gp.GeoDataFrame.from_file(river_shp_whl)
      ## inspired from https://stackoverflow.com/q/49948876
      # create bounding box for each polygon
      bbox = dfR.bounds
      bbox.head(10)
      dfR.insert(7,'Xmin',bbox.minx)
      dfR.insert(8,'Xmax',bbox.maxx) 
      dfR.insert(9,'Ymin',bbox.miny) 
      dfR.insert(10,'Ymax',bbox.maxy)
      dfR.head(10)
      dfR =dfR.rename(columns={'Z min (m)':'Z_min_m','Z max (m)':'Z_max_m','Area (km2)':'Area_km2','Perimeter':'Perimeter_m','X Center':'X_Center','Y Center':'Y_Center'})
      # convert 3D to 2D
      dfR.geometry = convert_3D_2D(dfR.geometry)
      dfR.to_csv(pathEditedRivers,mode = 'w', index=False)
      # read the csv and insert into the table
      with open(pathEditedRivers,encoding="utf8") as csvfile1:
        reader = csv.DictReader(csvfile1, delimiter = ',')
        for row in reader:
          #print (row)
          sql_statement_R = "INSERT IGNORE INTO riverShp(Z_min_m, Z_max_m, Perimeter_m, Area_km2, X_Center, Y_Center, Xmin, Xmax, Ymin, Ymax, geometry) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, ST_PolyFromText(%s,0))"
          cur = conn.cursor()
          cur.executemany(sql_statement_R,[(row['Z_min_m'], row['Z_max_m'], row['Perimeter_m'], row['Area_km2'], row['X_Center'], row['Y_Center'], row['Xmin'], row['Xmax'], row['Ymin'], row['Ymax'], row['geometry'])])
          print(sql_statement_R)
          conn.escape_string(sql_statement_R)
          conn.commit()
          stop = time.time()
          elapsed = stop - start
          if elapsed < 60:
            print("River_Poly edited and inserted into the DB, it took {0:0.2f}s.".format(elapsed))
          elif elapsed < 3600:
            mins = int(elapsed/60)
            seconds = int(elapsed - 60*mins)
            print("River_Poly edited and inserted into the DB, it took {}mins {}s.".format(mins, seconds))
          else:
            hours = int(elapsed/3600)
            mins = int((elapsed - 3600*hours) / 60)
            seconds = int(elapsed - 3600*hours - 60*mins)
            print("River_Poly edited and inserted into the DB, it took {}hours {}mins {}s.".format(hours, mins, seconds))

