import folium
import pandas as ps

data = ps.read_csv("Volcanoes.txt")
lat = list(data["LAT"])
lon = list(data["LON"])
elev = list(data["ELEV"])
name = list(data["NAME"])

html = """<h4>Volcano information:</h4>
<pre>
Height: %s m
Name: %s
</pre>

"""

def color_producer(elevation):
    if elevation<1000: 
        return 'green'
    elif 1000 <= elevation <3000:
        return 'orange'
    else: return 'red'

    

map = folium.Map(location=[38.58,-99.09], zoom_start=6, tiles = "Stamen Terrain")

fgv = folium.FeatureGroup(name="Volcanoes")
fgp = folium.FeatureGroup(name="Population")



fgp.add_child(folium.GeoJson(data=open('world.json','r',encoding='utf-8-sig').read(),
style_function=lambda x:{'fillColor':'green' if x['properties']['POP2005']<10000000 else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red'}))

for lt, ln, el,nm in zip(lat, lon, elev,name):
    iframe = folium.IFrame(html=html % (str(el),nm), width=200, height=100)
    fgv.add_child(folium.CircleMarker(location=[lt, ln],radius = 6, popup=folium.Popup(iframe), fill_color=color_producer(el),color='grey',fill = True,fill_opacity=0.7 ))



map.add_child(fgv)
map.add_child(fgp)
map.add_child(folium.LayerControl()) 
map.save("Map1.html")