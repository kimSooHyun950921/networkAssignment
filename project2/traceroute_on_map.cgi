#!/usr/bin/python3
import cgi,cgitb
import IpToGeo 
form = cgi.FieldStorage()

print("""
    <script>
    function add_marker(lat,lng){
       var position = new daum.maps.LatLng(lat,lng);
       var marker = new daum.maps.Marker({
            position:position});
        marker.setMap(map)
        positions.push(marker)
    }
    </script>
        """)

print("Content-type:text/html")
print()
print('<html>')
print('<head>')
print('<meta charset="utf-8">')
print("<title>Hello World</title>")
print("</head>")
print("<body>")
print("<h2> Traceroute -Visualize on Kakao Map </h2>")
print("<form method='get' action='traceroute_on_map.cgi'>")
print("<input type = 'text' name='target'/>","<input type='submit'/>")
print("</form>")
print('<div id="map" style="width:500px;height:400px;"></div>')
print('<script type="text/javascript" src="//dapi.kakao.com/v2/maps/sdk.js?appkey=6eead9af8af7072e366ce5b5e1d1a7e6"></script>')
print('<script> var container = document.getElementById("map");var options = {center:new daum.maps.LatLng(35.45,126.57),level:20};var map = new daum.maps.Map(container,options);</script>')

argv_data = form.getvalue('target')
toDia =  IpToGeo.ipTogeo()
geo_data = toDia.get_diameter(argv_data)

if argv_data is not None:
    print('<H2>Destionation : ',argv_data,'</H2>')
    count = 0
    print("<script> var positions = new Array();</script>")
    for geo in geo_data:
        if len(geo)>0 and geo['diameter'] is not None:
            ip_address = geo['IP']
            lat = geo['diameter']['latitude']
            longit = geo['diameter']['longitude']
            print('<div>','IP:(',geo['IP'],')-',end='')
            print('(latitude : ',lat,'',end='')
            print(', longitude : ',longit,')</div>')
            print("""<script>
                    add_marker(""",lat,""",""",longit,""");
                </script>""")
            count+=1
else:
    print("<H2>wrong input<H2>")



print("</body>")
print("</html>")
