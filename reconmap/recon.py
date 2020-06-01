import os
import webbrowser
import requests
from bs4 import BeautifulSoup
import folium
import pandas as pd
import numpy as numpy
import googlemaps


apikey = 'CiN%2FaMLI7zYq2yK3VRDZwXXkPLboTGDZ7XgC4MLBRJJUV%2FErugk0uaqW9PD5i5Ru2BpvZw8LLDXY1nrXe7TBDw%3D%3D'
params = '&pageNo=1&numOfRows=500'
#http://apis.data.go.kr/6260000/MaintenanceBusinessStatus/getMaintenanceBusiness?serviceKey=인증키&pageNo=1&numOfRows=5

url = 'http://apis.data.go.kr/6260000/MaintenanceBusinessStatus/getMaintenanceBusiness?serviceKey=' + apikey + params

gmaps_key = 'AIzaSyBsuUu5n3jUnV323BLr857OYzTs9SXwZwA'
gmaps = googlemaps.Client(key=gmaps_key)

res = requests.get(url)
soup = BeautifulSoup(res.content, 'html.parser')
data = soup.find_all('item')

addr_list=list()
step_list=list()

for item in data:
    #주소찾고 일원빼고 넣음
    addr = item.find('location').get_text() #주소
    addr_item = addr.split()
    if addr_item[-1] == '일원':
        del addr_item[-1]
    joined = ' '.join(addr_item)
    addr_list.append(joined)
        
    #사업추진단계 
    step = item.find('step').get_text() #진행수준
    step_list.append(step)

df = pd.DataFrame({'Address':addr_list, 'Step':step_list})

# for i in range(len(total_list)):
#     info = {'Address' : total_list[i][0], 'Step' : total_list[i][1]}

lat = []
lng = []

for i in range(181):
    gmaps_output = gmaps.geocode(df['Address'][i])
    location_output = gmaps_output[0].get('geometry')
    lat.append(location_output['location']['lat'])
    lng.append(location_output['location']['lng'])

df['lat'] = lat
df['lng'] = lng

mapping = folium.Map(location = [df['lat'].mean(), df['lng'].mean()], zoom_start=11)

for i in range(180):
    folium.Marker([df['lat'][i], df['lng'][i]], popup=df['Address'][i]).add_to(mapping)

filepath=r"C:\Users\USER\Desktop\SWEN\reconmap\recon.html"
mapping.save(filepath)
webbrowser.open('file://'+filepath)