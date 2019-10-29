import pandas as pd 
import folium

readLake = r"D:\data\final_files\Lake\LakeFinal.csv"
data = pd.read_csv(readLake)


readLake = r"D:\data\final_files\River\River_geofabriks.csv"
fe = pd.read_csv(readLake)

m = folium.Map(location=[20,0], tiles="Mapbox Bright", zoom_start=2)
 
# I can add marker one by one on the map
for i in range(0,len(data)):
   folium.Circle(
      location=[data.iloc[i]['longitude'], data.iloc[i]['latitude']],
      popup=data.iloc[i]['name'],
      radius=data.iloc[i]['feature_code']*10000,
      color='crimson',
      fill=True,
      fill_color='crimson'
   ).add_to(m)


# Save it as html
m.save(r'D:\data\final_files\Lake\mymap.html')

d = pd.read_csv(readLake)
d.head(10)
d.count()
d.feature_class.count()
## how many features does each country have ??
d.groupby('country').count()[['feature_code']]
## how many features are from geofabriks and geonames ??
d.groupby('source').count()[['feature_code']]
## how many Hydro features does each continent have ??
f = d.groupby('continent').count()[['feature_code']]
r = d.groupby('Africa').count()[['feature_code']]

import numpy as np
import matplotlib.pyplot as plt
# Make fake dataset
height = [3, 12, 5, 18, 45]
bars = ('A', 'B', 'C', 'D', 'E')
y_pos = np.arange(len(bars))
# Create horizontal bars
plt.barh(y_pos, height)
# Create names on the y-axis
plt.yticks(y_pos, bars)
# Show graphic
plt.show()

r = d.feature_code.count()
Africa = r-33687/8 *100
Antarctica  =r/230
Asia=r/127817
Europe=r/435045
North=r/507742
Oceania=r/17648
Sevenseas=r/196
South =r/31156

r1 = d.continent

import matplotlib.pyplot as plt
# create data
names='Africa', 'Antarctica', 'Asia', 'Europe', 'North America ','Oceania','Seven seas','South America',
size=[Africa,Antarctica,Asia,Europe,North,Oceania,Sevenseas,South]
# Create a circle for the center of the plot
my_circle=plt.Circle( (0,0), 0.7, color='white')
# Give color names
plt.pie(size, labels=names, colors=['red','green','blue','skyblue','red','green','blue','skyblue'])
p=plt.gcf()
p.gca().add_artist(my_circle)
plt.show()

# Custom colors --> colors will cycle
plt.pie(size, labels=names, colors=['red','green'])
p=plt.gcf()
p.gca().add_artist(my_circle)
plt.show()
from palettable.colorbrewer.qualitative import Pastel1_7
plt.pie(size, labels=names, colors=Pastel1_7.hex_colors)
p=plt.gcf()
p.gca().add_artist(my_circle)
plt.show()


## counting feature_code in diefferent ways ?
d['feature_code'].value_counts()
d['feature_code'].value_counts().max()
d['feature_code'].value_counts().min()
d['feature_code'].describe()

## get the top country 
def get_top_feature_code(d):
    return d['feature_code'].value_counts()

def get_top_country(d):
    return d['country'].value_counts()

def get_top_continent(d):
    return d['continent'].value_counts()

country = d.groupby('country').apply(get_top_feature_code) ## all the feature_code under a country and their counts
country.to_csv(r"D:\data\final_files\Lake\groupFeatureByCountry.csv",mode = 'w', index=False)
continent = d.groupby('continent').apply(get_top_feature_code) ## all the feature_code under a continents and their counts
continent.to_csv(r"D:\data\final_files\Lake\groupFeatureByContinent.csv",mode = 'w', index=False)
d.groupby('feature_code').apply(get_top_country) ## all countries and tehir counts under each feature_code
d.groupby('feature_code').apply(get_top_continent)## all the continents and their count under feature_code
## or 
d.groupby(['feature_code','country']).size()
d.groupby(['country','feature_code']).size()

## group the lakes categories into Lake
findL = ['LK','LKI','LKS','LKSI','LKN','LKNI','LKSN','LKSNI','LKO','LKOI','LKC','LKX','RSV','RSVI','PND','PNDI','PNDS','PNDSI','PNDSN','WTRH','MRSH','SPNG']
replaceL = ['lake','intermittent_lake','lakes','intermittent_lakes','salt_lake','intermit_salt_lake','salt_lakes','intermittent_salt_lakes','oxbow_lake','intermittent_oxbow_lake','crater_lake','section_of_lake','reservoir','intermittent_reservoir','pond','intermittent_pond','ponds','intermittent_ponds','salt_ponds','waterholes','marshes','spring']
    

findR = ['STM','STMS','STMD','STMI','STMX' ,'STMIX','STMM','SWMP','WTRC']
replaceR = ['stream','streams','distributary','intermittent_stream','section_of_stream','section_of_intermittent_stream','stream_mouths','swamp','watercourse']

## charts for py graphsS
## https://python-graph-gallery.com/all-charts/

d.groupby("country")['feature_code'].plot(kind='bar')