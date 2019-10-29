#--------------------------------------------------------------------------------------------------#
#                      Script to unzip and extract files from GEONAMES                             #
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

#-----------------------------------------------------------#
#              Downloading and updating files               #
#-----------------------------------------------------------#
'''
countryCodeTxt      - text file containing the geonames country code
                      change this path based on the location of 'geonames_country_code.txt'

zipfileGeoPath      - path to the folder containing the .zip files
                      change this path based on the location of the geonames .zip files

Line 69-83 : 
     Condition based on size of the files

     if website file size = local file size --- NO CHANGE
     if website file size > local file size --- DOWNLOAD the files

'''
## to check if the file exists oelse raise error
def fileExits(fileCheck):
     if not os.path.exists(fileCheck):
          raise IOError('{:s} does not exist.'.format(fileCheck))
     else:
          print("Ok")

start = time.time()
## file containing the country code
countryCodeTxt = "D:/data/geonames_country_code.txt"
zipfileGeoPath = "D:/data/geonames/zipFiles/"
fileExits(zipfileGeoPath)
fileExits(countryCodeTxt)
f = open(countryCodeTxt)
NamesOfFile = f.readlines()

for x in NamesOfFile:
     link = "http://download.geonames.org/export/dump/"+ x
     print("Opening url:", link)
     try:
          site = urllib.request.urlopen(link)
          print("Success, Able to open",site)
     except:
          print("Error, Unable to Open",site)
     meta = site.info()
     ## getting file size of the file from website
     web_len = meta.get("Content-length")
     print ("Content-Length of file "+ x +"from website:",web_len)
     filesLocal = zipfileGeoPath+ x
     ## getting file size of the file from local folder
     paths = os.path.join(filesLocal)
     string = paths.rstrip('\n')
     f = open(string,"rb")
     local_len = len(f.read())
     print("Size of the Old file from local folder "+ x +":",local_len)
     f.close()
     difference_size = int(local_len) - int(web_len)
     if difference_size == 0:
          print("File Size is EQUAL, NO CHANGE")
     elif difference_size < 0:
          print("File needs to be UPDATED")
          ## download the updated file 
          f = open(string,"wb")
          f.write(site.read())
          site.close()
          f.close()
          # reading the file size after downloading 
          f = open(string, "rb")
          print ("File on disk after download:",len(f.read()))
          f.close()
          print ("os.stat().st_size returns:", os.stat(string).st_size)
    
     stop = time.time()
     elapsed = stop - start
     if elapsed < 60:
          print("File updating process finished, it took {0:0.2f}s.".format(elapsed))
     elif elapsed < 3600:
          mins = int(elapsed/60)
          seconds = int(elapsed - 60*mins)
          print("File updating process finished, it took {}mins {}s.".format(mins, seconds))
     else:
          hours = int(elapsed/3600)
          mins = int((elapsed - 3600*hours) / 60)
          seconds = int(elapsed - 3600*hours - 60*mins)
          print("File updating process finished, it took {}hours {}mins {}s.".format(hours, mins, seconds))


#------------------------------------------------#
#              Unzipping .zip files              #
#------------------------------------------------#
'''
zipfileGeoPath     - path to the folder containing the .zip files
                     change this path based on the location of the geonames .zip files

unzipFileGeoPath   - path to the folder containing the extracted files
                     change this path folder based on the location of where you want to extract your files

'''
start = time.time()
unzipFileGeoPath = "D:/data/geonames/extracted"
fileExits(unzipFileGeoPath)
pattern = '*.zip'
## looping to read all the .zip files in the 'zipfileGeoPath' folder
for root, dirs, files in os.walk(zipfileGeoPath):
    for filename in fnmatch.filter(files, pattern):
        geo_zip_paths = (os.path.join(root, filename))
        print(geo_zip_paths)
        zipfile.ZipFile(geo_zip_paths).extractall(os.path.join(unzipFileGeoPath,os.path.splitext(filename)[0]))
        stop = time.time()
        elapsed = stop - start
        # Pretty print the time elapsed
        if elapsed < 60:
            print("Process finished, it took {0:0.2f}s. to unzip".format(elapsed))
        elif elapsed < 3600:
            mins = int(elapsed/60)
            seconds = int(elapsed - 60*mins)
            print("Process finished, it took {}mins {}s. to unzip".format(mins, seconds))
        else:
            hours = int(elapsed/3600)
            mins = int((elapsed - 3600*hours) / 60)
            seconds = int(elapsed - 3600*hours - 60*mins)
            print("Process finished, it took {}hours {}mins {}s. to unzip".format(hours, mins, seconds))


#------------------------------------------------#
#                Remove files                    #
#------------------------------------------------#
'''
Remove readme.txt files and .csv if exists

Line 157-160 inspired from source :
https://stackoverflow.com/a/678266/10546341
https://stackoverflow.com/a/8384786/10546341

readmeFiles    - file list containing 'readme.txt' file paths
csvEndFile     - file list containing '.csv' file paths

'''
for root, dirs, files in os.walk(unzipFileGeoPath):
    for file in files:
        if file.endswith("readme.txt"):
            readmeFiles = os.path.join(root, file)
            #print(readmeFiles)
            os.remove(readmeFiles)
            head,tail = os.path.split(readmeFiles)
            base=os.path.basename(head)
            #os.path.splitext(base)[0]
            print(os.path.splitext(base)[0]+" file removed...")
        elif file.endswith(".csv"):
            csvEndFile = os.path.join(root, file)
            print(csvEndFile)
            os.remove(csvEndFile)
            print("Removed .csv files...")
