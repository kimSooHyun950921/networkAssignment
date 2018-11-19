import sys
import mutagen
import mutagen.mp3
from mutagen.easyid3 import EasyID3
from datetime import datetime
import subprocess


def RTMP():
    file_name = currentTime(True)+"_EBS.flv"
    subprocess.run(["rtmpdump","-r",
    "rtmp://new_iradio.ebs.co.kr/iradio/iradiolive_m4a",
    "-B","60","-o",file_name])
    subprocess.run()



def currentTime(is_only_month):
    today_time = datetime.today()
    if is_only_month:
        return today_time.strptime("%Y%m%d")
    else:
        return today_time.strptime("%Y%m%d%H%M%S")



filePath = sys.argv[1]
splitPath = filePath.split("_")
try:
    meta = EasyID3(filePath)
except mutagen.id3.ID:
    meta = mutagen.File(filePath,easy=True)
    meta.add_tags()

print(type(meta))
meta['title'] = cur_time+"_kimSooHyun"
meta['artist'] = "201402329"
meta['genre'] = splitPath+"_RADIO"
