import folium
import pandas as ps
from branca.element import Template, MacroElement

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

template = """
{% macro html(this, kwargs) %}

<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">

  <script src="https://code.jquery.com/jquery-1.12.4.js"></script>
  <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
  
   <script>
  $( function() {
    $( "#maplegend" ).draggable({
                    start: function (event, ui) {
                        $(this).css({
                            right: "auto",
                            top: "auto",
                            bottom: "auto"
                        });
                    }
                });
});

  </script>
</head>
<body>

 
<div id='maplegend' class='maplegend' 
    style='position: absolute; z-index:9999; border:2px solid grey; background-color:rgba(255, 255, 255, 0.8);
     border-radius:6px; padding: 10px; font-size:14px; right: 20px; bottom: 20px;'>
     
<div class='legend-title'>Legenda </div>
<div class='legend-scale'>
  <ul class='legend-labels'>
    <li><span style='background:red;opacity:0.7;'></span>Veće od 10 mil stanovnika</li>
    <li><span style='background:orange;opacity:0.7;'></span>Veće od 10 mil i manje od 20 mil stanovnika</li>
    <li><span style='background:green;opacity:0.7;'></span>Manje od 10 mil stanovnika</li>
    <li><span style='background:red;opacity:0.7;'></span>Vulkani višlji od 3000m</li>
    <li><span style='background:orange;opacity:0.7;'></span>Vulkani višlji od 1000m i manji od 30000m</li>
    <li><span style='background:green;opacity:0.7;'></span>Vulkani višlji od 1000m</li>


  </ul>
</div>
</div>
 
</body>
</html>

<style type='text/css'>
  .maplegend .legend-title {
    text-align: left;
    margin-bottom: 5px;
    font-weight: bold;
    font-size: 90%;
    }
  .maplegend .legend-scale ul {
    margin: 0;
    margin-bottom: 5px;
    padding: 0;
    float: left;
    list-style: none;
    }
  .maplegend .legend-scale ul li {
    font-size: 80%;
    list-style: none;
    margin-left: 0;
    line-height: 18px;
    margin-bottom: 2px;
    }
  .maplegend ul.legend-labels li span {
    display: block;
    float: left;
    height: 16px;
    width: 30px;
    margin-right: 5px;
    margin-left: 0;
    border: 1px solid #999;
    }
  .maplegend .legend-source {
    font-size: 80%;
    color: #777;
    clear: both;
    }
  .maplegend a {
    color: #777;
    }
</style>
{% endmacro %}"""

def color_producer(elevation):
    if elevation<1000: 
        return 'green'
    elif 1000 <= elevation <3000:
        return 'orange'
    else: return 'red'

    

map = folium.Map(location=[38.58,-99.09], zoom_start=6, tiles = "Stamen Terrain")

fgv = folium.FeatureGroup(name="Vulkani")
fgp = folium.FeatureGroup(name="Populacija")



fgp.add_child(folium.GeoJson(data=open('world.json','r',encoding='utf-8-sig').read(),
style_function=lambda x:{'fillColor':'green' if x['properties']['POP2005']<10000000 else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red'}))

for lt, ln, el,nm in zip(lat, lon, elev,name):
    iframe = folium.IFrame(html=html % (str(el),nm), width=200, height=100)
    fgv.add_child(folium.CircleMarker(location=[lt, ln],radius = 10, popup=folium.Popup(iframe), fill_color=color_producer(el),color='grey',fill = True,fill_opacity=0.7 ))


macro = MacroElement()
macro._template = Template(template)


map.get_root().add_child(macro)
map.add_child(fgp)
map.add_child(fgv)
map.add_child(folium.LayerControl()) 
map.save("Map1.html")