import sys
import subprocess as sp
import pygeoip 
import re

class ipTogeo():

    def __init__(self):
        self.url = sys.argv[1]
        self.GeoToIP = pygeoip.GeoIP('GeoLiteCity.dat')


    def run_traceroute(self):
        proc = sp.Popen(["traceroute",self.url],stdout = sp.PIPE)
        stdout_data= proc.stdout
        return stdout_data
      
    def change_Diameter(self,data):
        diameter = dict()
        geoIPInfo = dict()

        if len(data)>0:
            geoIPInfo.update({'IP':data[0]})
            result = self.GeoToIP.record_by_addr(data[0])
            if result is not None:
                diameter.update({'latitude':result['latitude']})
                diameter.update({'longitude': result['longitude']})
                geoIPInfo.update({'diameter':diameter})
            else:
                geoIPInfo.update({'diameter': None})

        return geoIPInfo


    
    def print_result(self,geo_data):
        if geo_data == "start":
            print("[Destination] ",self.url)
        elif len(geo_data)>0:
            if geo_data['diameter'] is None:
                print("[IP] ",geo_data['IP'],' - No Geolocation Info.')
            else:
                lat = geo_data['diameter']
                lon = geo_data['diameter']
                print("[IP] ",geo_data['IP']," - Lat : ",lat['latitude'],' Lon: ' ,lon['longitude'])

        return

    def get_IP(self,line):
        split_data = line.decode('utf-8').split()
        need_data = split_data[2]
        filter_data = re.compile("[0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}")
        IP = filter_data.findall(need_data)
        return IP

    def main(self):
        data = self.run_traceroute()
        count = 0
        self.print_result("start")
        for line in data:
            split_data = self.get_IP(line)
            diameter = self.change_Diameter(split_data)
            self.print_result(diameter)

if __name__ == '__main__':
    ip2geo = ipTogeo()
    ip2geo.main()
