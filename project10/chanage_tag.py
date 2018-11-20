"""
    라디오 녹음하는 파이썬코드
Usage:
   python3 change_tag.py

"""
from datetime import datetime
import subprocess
import mutagen
import mutagen.mp3
from mutagen.easyid3 import EasyID3


FILE_PATH = '/home/kimsoohyun/Desktop/network/project10/mp3_file'
FILE_FLV = ".flv"
FILE_MP3 = ".mp3"
FILE_EBS = "_EBS"
FILE_KBS = "_KBS"

def rtmp():
    """
    EBS방송을 녹음하는 함수 .flv파일을 변환 하고 저장한다.
    :return: Subprocess의 에러 유무
    """

    file_name = FILE_PATH+__get_current_time('day') + FILE_EBS
    try:
        subprocess.run(["rtmpdump", "-r",
                        "rtmp://new_iradio.ebs.co.kr/iradio/iradiolive_m4a",
                        "-B", "60", "-o", file_name+FILE_FLV])
        subprocess.run(["ffmpeg", "-i", file_name+FILE_FLV, "-acodec",
                        "mp3", file_name+FILE_MP3])
        __change_meta_data(file_name+FILE_MP3)
        return True
    except subprocess.CalledProcessError as sub_exception:
        print("ERROR With RTMP:", sub_exception)
        return False

def mpc():
    """KBS 방송을 녹음하는 함수"""
    file_name = FILE_PATH+__get_current_time('day') + FILE_KBS+FILE_MP3
    try:
        url_KBS = 'http://onair.kbs.co.kr/index.html?sname=onair&stype=live&ch_code=24&ch_type=radioList'
        curl_KBS = 'curl -s '+url_KBS+'| grep service_url | tail -1 | cut -d\\" -f 16 | cut -d\\\\ -f 1'
        subprocess.run("mplayer $("+curl_KBS+") -ao pcm:file="+file_name+" -vc dummy -vo null", shell=True)
        __change_meta_data(file_name)
        return True
    except subprocess.CalledProcessError as sub_exception:
        print("ERROR with mpc:", sub_exception)
        return False


def __get_current_time(is_month):
    """
    현재시간을 구하는 함수
    :param:moth일때는 true 시간만 구할때는 false bool값
    :return:year일때는 년월만, 그렇지 않은 경우 초까지 반환
    """
    today_time = datetime.today()
    if is_month == 'month':
        return today_time.strptime("%Y%m%d")
    return today_time.strptime("%Y%m%d%H%M%S")

def __get_date_from_file(file_path):
    """
    KBS인지 EBS인지 확인하는 함수
    :param: mp3파일 이름
    :return: KBS or EBS
    """
    return file_path.split('_')[0][0:2]

def __change_meta_data(file_path):
    """
    mp3파일의 메타 데이터를 바꾼다.
    :param: mp3파일 이름
    """
    try:
        meta = EasyID3(file_path)
    except mutagen.id3.ID3NoHeaderError:
        meta = mutagen.File(file_path, easy=True)
        meta.add_tags()

    print(type(meta))
    meta['title'] = __get_current_time('month')+"_kimSooHyun"
    meta['artist'] = "201402329"
    meta['genre'] = __get_date_from_file(file_path)+"_RADIO"

def execute():
    """
    rtmp와 mpc를 실행하는 부분
    """
    rtmp()
    mpc()

def main():
    execute()
main()
