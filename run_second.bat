@echo off
title This is my first bat script
echo welcome
python C:/Users/ssivakumar/Desktop/dscs/lake_shapefile.py %*
python C:/Users/ssivakumar/Desktop/dscs/river_shapefile.py %*
python C:/Users/ssivakumar/Desktop/dscs/lakept_2_DB.py %*
python C:/Users/ssivakumar/Desktop/dscs/riverpt_2_DB.py %*
python C:/Users/ssivakumar/Desktop/dscs/sql_queries.py %*
pause