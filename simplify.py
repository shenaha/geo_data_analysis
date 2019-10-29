from shapely.geometry import Polygon
import pandas as pd, numpy as np, matplotlib.pyplot as plt
from shapely.geometry import LineString
from time import time
import geopandas as gpd
shp = r"D:\script\hydro-CEM\output\62\countour.shp"

d = gpd.read_file(shp)
x = d.buffer(0.0001)
#x.area
#len(x.exterior.geometry)
tolerance = 0.00005
simplified = x.simplify(tolerance, preserve_topology=True)
simplified.to_file(r"D:\script\hydro-CEM\output\62\simplified000i_000005.shp")


