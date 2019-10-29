@echo off
title This is my first bat script
echo welcome
python C:/Users/ssivakumar/Desktop/dscs/geonames_unzip_deletefiles.py %*
python C:/Users/ssivakumar/Desktop/dscs/geofabrik_unzip_deletefiles.py %*
python C:/Users/ssivakumar/Desktop/dscs/geonamesWaterExtraction.py %*
python C:/Users/ssivakumar/Desktop/dscs/geofabriksWaterExtraction.py %*
python C:/Users/ssivakumar/Desktop/dscs/MergeFiles.py %*
pause