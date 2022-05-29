from cgitb import small
import geopandas as gpd
import numpy as np
import folium
import json
import pandas
from branca.element import Figure
import pandas as pd
import math



# Enable fiona driver
gpd.io.file.fiona.drvsupport.supported_drivers['KML'] = 'rw'

# read file
my_map = gpd.read_file('vo_NEA_EIRP.kml', driver='KML')


df = gpd.GeoDataFrame(my_map)


# check indices is between 46 & 48
# print(df.loc[(df['Name'] == '46.0')])
# print(df.loc[(df['Name'] == '48.0')])


# assign var for signal 46
signal_46 = df.iloc[434:686]


# extract geomtery
dots = signal_46['geometry']


long = []
lat = []
# getting the coordinates
for points in dots:
    dots_list = list(points.coords)
    for item in dots_list:
        long.append(item[0])  # selecting longitude
        lat.append(item[1])  # selecting latitude

#append to np array
longitude=np.array(long)
latitude=np.array(lat)
coordinates=np.array(list(zip(longitude,latitude))) 

area1=[]
area2=[]
area3=[]
area4=[]
mini_area=[]

def find_coordinates1(i,index):
    for item in coordinates:
        if item[index]>i:
            area1.append(item)
find_coordinates1(53,1)


def find_coordinates2(j,i,index):
    for item in coordinates:
        if j<item[index]<i:
            area2.append(item)
find_coordinates2(32,53,1)

def find_coordinates3(low_bound,i,high_bound,low_bound2,j,high_bound2,area):
    for item in coordinates:
        if low_bound<item[i]<high_bound and low_bound2<item[j]<high_bound2:
            area.append(item)

find_coordinates3(28,1,32,99,0,117,area3)
extract_coord3=sorted(area3,key=lambda l:l[0])

find_coordinates3(0,1,27, 99,0,122,area4)
extract_coord4=sorted(area4,key=lambda l:l[1])

find_coordinates3(15,1,22,131,0,136,mini_area)


def averageOfList(numOfList):
    avg = sum(numOfList) / len(numOfList)
    return avg

center_point1=averageOfList(area1)
center_point2=averageOfList(area2)
center_mini=averageOfList(mini_area)

# center_point4=averageOfList(area4)
# try azimuth method here
azimuth1=[]
azimuth2=[]
azimuthmini=[]

def azimuthAngle(center_point,azimuth,area):
    angle = 0.0
    for item in area:
        dx = item[0] - center_point[0]
        dy = item[1] - center_point[1] 
        if item[0] == center_point[0]:
            angle = math.pi / 2.0
            if item[1] == center_point[1] :
                angle = 0.0
            elif item[1] < center_point[1] :
                angle = 3.0 * math.pi / 2.0
        elif item[0] > center_point[0] and item[1] > center_point[1]:
            angle = math.atan(dx / dy)
        elif item[0] > center_point[0] and item[1] < center_point[1] :
            angle = math.pi / 2 + math.atan(-dy / dx)
        elif item[0] < center_point[0] and item[1] < center_point[1] :
            angle = math.pi + math.atan(dx / dy)
        elif item[0] < center_point[0] and item[1] > center_point[1] :
            angle = 3.0 * math.pi / 2.0 + math.atan(dy / -dx)
        azimuth.append(angle * 180 / math.pi)
azimuthAngle(center_point1,azimuth1,area1)
azimuthAngle(center_point2,azimuth2,area2)
azimuthAngle(center_mini,azimuthmini,mini_area)

angle1=np.array(azimuth1)
angle2=np.array(azimuth2)
mini=np.array(azimuthmini)



#combine angle with coordinates
coordinates_angle1=np.array(list(zip(angle1,area1)),dtype=object) 
coordinates_angle2=np.array(list(zip(angle2,area2)),dtype=object) 
coordinates_angle_mini=np.array(list(zip(mini,mini_area)),dtype=object) 


#sort angle
sorted_angle1=coordinates_angle1[np.argsort(coordinates_angle1[:, 0])]
sorted_angle2=coordinates_angle2[np.argsort(coordinates_angle2[:, 0])]
sorted_mini=coordinates_angle_mini[np.argsort(coordinates_angle_mini[:, 0])]


extract_coord1=[]
extract_coord2=[]
extract_mini=[]


for item in sorted_angle1:
    extract_coord1.append(item[1])

for item2 in sorted_angle2:
    extract_coord2.append(item2[1])

for item in sorted_mini:
    extract_mini.append(item[1])

# print(len(extract_coord1))
right1=extract_coord1[0:14]
left1=extract_coord1[14:44]

#slice into 2 parts of area2
right2=extract_coord2[0:49]
left2=extract_coord2[52:117]

total1=extract_coord4+extract_coord3+left2+left1+right1+right2
center_point3=averageOfList(total1)

# angka=[]
# for x in extract_coord2:
#     angka.append(x[0])
# print(angka.index(145.9792))
# Create the map and add the line

# print(coordinates_angle)
# print(coordinates_angle.shape)
# for i in range(len(coordinates_angle)):
#     np.sort(coordinates_angle[1].any())


# center_point=[]
# for item in area1:
#     print(item)

# zipped into one
long_lat = zip(long,lat)
zipped_list = list(long_lat)

array_order=sorted(zipped_list)
# print(array_order)

# find_index=array_order.index((132.0074,20.2257))
# print(find_index)
# print(array_order)

small_array=[array_order[212:215],array_order[218:219],array_order[220:223],array_order[230:231],array_order[234:238],array_order[240:243],array_order[250:252],array_order[254:257],array_order[260:261],array_order[266:269],array_order[272:275]]
# print(small_array)
# print(small_array[0])
# print(small_array[1])
# print(small_array[2])
# print(small_array[3])
# print(small_array[4])
# print(small_array[5])
# print(small_array[6])
# print(small_array[7])
# print(small_array[8])
# print(small_array[9])
# print(small_array[10])

for i in range(0,len(zipped_list)):
    for j in range(0,len(small_array)):
        if zipped_list[i]==small_array[j]:
            zipped_list[i].pop()
           

#https://linuxtut.com/en/b375e5fa578eb8880662/
import simplekml
kml = simplekml.Kml()

# Create an instance of Kml
kml = simplekml.Kml(open=1)

# create linestring from center point to every point
for item in extract_mini:
    linestring = kml.newlinestring(name="A Line")
    linestring.coords = [(center_mini),(item)]
    kml.save('try.kml')

# creating points
# for row in coordinates:
#     ls = kml.newpoint(name="signal46")
#     ls.coords = [(row[0],row[1])]
#     kml.save('upper.kml')


# json_object = json.dumps(zipped_list, indent = 11) # Serializing json
# with open("sample.json", "w") as file: # writing json file
#     json.dump(zipped_list,file,indent=1)



