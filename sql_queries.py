#---------------------------------------------------------------------#
#                    One time executable SQL Query                    #
#---------------------------------------------------------------------#

import csv
import time
import datetime
import MySQLdb
import pandas as pd 
import geopandas as gpd
from geopandas.tools import sjoin
from shapely.geometry import Point

## Add geometry column within the SQL and download it ity less time consuming 
conn = MySQLdb.connect(host="localhost", port=3306, user="root", passwd="Pa$$w0rd", db="geonames", charset="utf8")
cur = conn.cursor()
#
## add geometry column in points table
#cur.execute('SET SQL_SAFE_UPDATES = 0;')
cur.execute('ALTER TABLE geonames.lakepoints ADD COLUMN IF NOT EXISTS coords geometry AFTER longitude;')
cur.execute('UPDATE geonames.lakepoints SET IF NOT EXISTS coords = POINT(longitude,latitude);')
cur.execute('ALTER TABLE geonames.riverpoints ADD COLUMN IF NOT EXISTS coords geometry AFTER longitude;')
cur.execute('UPDATE geonames.riverpoints SET IF NOT EXISTS coords = POINT(longitude,latitude);')
#cur.execute('SET SQL_SAFE_UPDATES = 1;')

## create index 
cur.execute('CREATE INDEX index_lake ON geonames.lakepoints(ID_source);')
cur.execute('CREATE INDEX index_lake ON geonames.riverpoints(ID_source);')

## join tables based on condition
cur.execute('CREATE TABLE geonames.joiningTable2 SELECT Lake_ID, Lakept_ID, ID_source FROM geonames.lakepoints, geonames.lakeshp WHERE (latitude > Ymin and latitude < Ymax) and (longitude > Xmin and longitude < Xmax);')                                                                                                                                                            
#set_1 = cur.fetchall()
#
## create a View containing the final table
cur.execute("CREATE VIEW `geonames`.`current_lakes1` AS"
    "SELECT"
        "`l`.`Lake_ID` AS `Lake_ID`,"
        "`j`.`Lakept_ID` AS `Lakept_ID`,"
        "`p`.`name` AS `name`,"
        "`p`.`ID_source` AS `ID_source`,"
        "`p`.`feature_class` AS `feature_class`,"
        "`p`.`feature_code` AS `feature_code`,"
        "`l`.`X_Center` AS `X_Center`,"
        "`l`.`Y_Center` AS `Y_Center`,"
        "`p`.`latitude` AS `latitude`,"
        "`p`.`longitude` AS `longitude`,"
        "l`.`geometry` AS `geometry`,"
        "`p`.`source` AS `source`"
    "FROM"
        "(`geonames`.`lakeshp` `l`"
        "LEFT JOIN `geonames`.`joiningtable2` `j` ON ((`l`.`Lake_ID` = `j`.`Lake_ID`))"
        "LEFT JOIN `geonames`.`lakepoints` `p` ON ((`j`.`Lakept_ID` = `p`.`Lakept_ID`)));")


## if called externally -- run once
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'Pa$$w0rd';
## set coord 
ALTER TABLE geonames.lakepoints ADD COLUMN coords geometry AFTER longitude;
UPDATE geonames.lakepoints SET coords = POINT(longitude,latitude);
## combine data 
CREATE TABLE geonames.joinLake SELECT Lake_ID, Lakept_ID, name, ID_source FROM geonames.lakepoints, geonames.lakeshp WHERE (latitude > Ymin and latitude < Ymax) and (longitude > Xmin and longitude < Xmax);                                                                                                                                                                                             
## view 
CREATE VIEW `geonames`.`current_lake` AS
    SELECT 
        `l`.`Lake_ID` AS `Lake_ID`,
        `j`.`Lakept_ID` AS `Lakept_ID`,
        `p`.`name` AS `name`,
        `p`.`ID_source` AS `ID_source`,
        `p`.`feature_class` AS `feature_class`,
        `p`.`feature_code` AS `feature_code`,
        `l`.`Z_m` AS `Z_m`,
        `l`.`Perimeter_m` AS `Perimeter_m`,
        `l`.`Area_km2` AS `Area_km2`,
        `l`.`X_Center` AS `X_Center`,
        `l`.`Y_Center` AS `Y_Center`,
        `p`.`latitude` AS `latitude`,
        `p`.`longitude` AS `longitude`,
        `p`.`country` AS `country`,
        `p`.`continent` AS `continent`,
        `l`.`geometry` AS `geometry`,
        `p`.`source` AS `source`,
        `p`.`modification_date` AS `modification_date`
        
    FROM
        (`geonames`.`lakeshp` `l`
        LEFT JOIN `geonames`.`joinLake` `j` ON ((`l`.`Lake_ID` = `j`.`Lake_ID`))
        Left JOIN `geonames`.`lakepoints` `p` ON ((`j`.`Lakept_ID` = `p`.`Lakept_ID`)))


########### RIVER
## set coord 
ALTER TABLE geonames.riverpoints ADD COLUMN coords geometry AFTER longitude;
UPDATE geonames.riverpoints SET coords = POINT(longitude,latitude);
## combine data 
CREATE TABLE geonames.joinRiver SELECT RiverID, Riverpt_ID, name, ID_source FROM geonames.riverpoints, geonames.rivershp WHERE (latitude > Ymin and latitude < Ymax) and (longitude > Xmin and longitude < Xmax);                                                                                                                                                                                             
## view 
CREATE VIEW `geonames`.`current_lake` AS
    SELECT 
        `s`.`RiverID` AS `RiverID`,
        `j`.`Riverpt_ID` AS `Riverpt_ID`,
        `r`.`name` AS `name`,
        `r`.`ID_source` AS `ID_source`,
        `r`.`feature_class` AS `feature_class`,
        `r`.`feature_code` AS `feature_code`,
        `s`.`Z_m` AS `Z_m`,
        `s`.`Perimeter_m` AS `Perimeter_m`,
        `s`.`Area_km2` AS `Area_km2`,
        `s`.`X_Center` AS `X_Center`,
        `s`.`Y_Center` AS `Y_Center`,
        `r`.`latitude` AS `latitude`,
        `r`.`longitude` AS `longitude`,
        `r`.`country` AS `country`,
        `r`.`continent` AS `continent`,
        `s`.`geometry` AS `geometry`,
        `r`.`source` AS `source`,
        `r`.`modification_date` AS `modification_date`
        
    FROM
        (`geonames`.`rivershp` `s`
        LEFT JOIN `geonames`.`joinRiver` `k` ON ((`s`.`RiverID` = `k`.`RiverID`))
        Left JOIN `geonames`.`riverpoints` `r` ON ((`k`.`Riverpt_ID` = `r`.`Riverpt_ID`)))