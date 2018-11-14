#!/usr/bin/python3
import cgi,cgitb
import IpToGeo 
form = cgi.FieldStorage()


print("Content-type:text/html")
print()
print('<html>')
print('<head>')
print('<meta charset="utf-8">')
print("<title>Hello World</title>")
print("</head>")
print("<body>")
print("<h2> Traceroute -Visualize on Kako Map </h2>")
print("<form method='get' action='hellothml.cgi'>")
print("<input type = 'text' name='target'/>","<input type='submit'/>")
print("</form>")
print('<div id="map" style="width:500px;height:400px;"></div>')
print('<script type="text/javascript" src="//dapi.kakao.com/v2/maps/sdk.js?appkey=6eead9af8af7072e366ce5b5e1d1a7e6"></script>')
print('<script> var container = document.getElementById("map");var options = {center:new daum.maps.LatLng(33.45,126.57),level:30};var map = new daum.maps.Map(container,options);</script>')

argv_data = form.getvalue('target')

toDia =  IpToGeo.ipTogeo()
result = toDia.get_diameter(argv_data)

print('<H2>Hello',argv_data,'</H2>')
print("</body>")
print("</html>")

