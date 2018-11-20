"""
    라디오 녹음하는 파이썬코드
Usage:
   python3 change_tag.py

"""
import subprocess
from datetime import datetime
import mutagen
import mutagen.mp3
from mutagen.easyid3 import EasyID3

FLV_PATH = "/home/kimsoohyun/Desktop/network/project10/flv_file/"
MP3_PATH = "/home/kimsoohyun/Desktop/network/project10/mp3_file/"
FILE_FLV = ".flv"
FILE_MP3 = ".mp3"
FILE_EBS = "_EBS"
FILE_KBS = "_KBS"
TIME_OUT = 20
RTMP_URL = "rtmp://new_iradio.ebs.co.kr/iradio/iradiolive_m4a"

def rtmp():
    """
    EBS방송을 녹음하는 함수 .flv파일을 변환 하고 저장한다.
    :return: Subprocess의 에러 유무
    """
    absolute_path = __get_current_time('day')+ FILE_EBS
    try:
        subprocess.run(["rtmpdump", "-r", RTMP_URL,
                        "-B", str(TIME_OUT), "-o", FLV_PATH+absolute_path+FILE_FLV])
        __flv_to_mp3(absolute_path)
        __change_meta_data(MP3_PATH+absolute_path+FILE_MP3)
    except subprocess.CalledProcessError as sub_exception:
        print("ERROR With RTMP:", sub_exception)

def mpc():
    """KBS 방송을 녹음하는 함수"""
    absolute_path = __get_current_time('day') + FILE_KBS
    print("CHECK", absolute_path)
    url_KBS = '\"http://onair.kbs.co.kr/index.html?sname=onair&stype=live&ch_code=24&ch_type=radioList\"'
    curl_KBS = 'curl -s '+url_KBS+'| grep service_url | tail -1 | cut -d\\" -f 16 | cut -d\\\\ -f 1'
    try:
        process = subprocess.Popen(
            "mplayer $("+curl_KBS+") -ao pcm:file="+FLV_PATH
            +absolute_path+FILE_FLV+" -vc dummy -vo null",
            shell=True)
        process.communicate(timeout=TIME_OUT)
    except subprocess.CalledProcessError as sub_exception:
        print("ERROR with mpc:", sub_exception)
    except subprocess.TimeoutExpired:
        print("TIME OUT")
        __force_kill()
        __flv_to_mp3(absolute_path)
        __change_meta_data(MP3_PATH+absolute_path+FILE_MP3)

def __flv_to_mp3(file_name):
    subprocess.run(["ffmpeg", "-i", FLV_PATH+file_name+FILE_FLV, "-acodec",
                    "mp3", MP3_PATH+file_name+FILE_MP3])

def __force_kill():
    """
    강제종료하는 함수
    subprocess로 ps를 불러와  mplayer의 PID를 확인 후,
    PID를  강제 종료 시킨다.
    """
    process_ids = __get_pid()
    for pid in process_ids:
        subprocess.run("kill -9 "+str(pid), shell=True)

def __get_pid():
    get_process = subprocess.check_output("ps | grep mplayer", shell=True)
    split_process = get_process.decode().split("\n")
    process_ids = list()
    for i in range(len(split_process)-1):
        result = split_process[i].split()
        process_ids.append(result[0])
    return process_ids


def __get_current_time(is_month):
    """
    현재시간을 구하는 함수
    :param:moth일때는 true 시간만 구할때는 false bool값
    :return:year일때는 년월만, 그렇지 않은 경우 초까지 반환
    """
    today_time = datetime.today()
    if is_month == 'month':
        return today_time.strftime("%Y%m%d")
    return today_time.strftime("%Y%m%d%H%M%S")

def __get_date_from_file(file_path, get_type):
    """
    KBS인지 EBS인지 확인하는 함수
    :param: mp3파일 이름
    :return: KBS or EBS
    """
    files = file_path.split('_')

    if get_type == "genre":
        return files[2][0:3]
    return files[1][5:]



def __change_meta_data(file_path):
    """
    mp3파일의 메타 데이터를 바꾼다.
    :param: mp3파일 이름
    """
    file_path = '{}/{}'.format(file_path.split("/")[-2],
                               file_path.split("/")[-1])
    print("NO", file_path)
    try:
        meta = EasyID3(file_path)
    except mutagen.id3.ID3NoHeaderError:
        print("CHECK", file_path)
        meta = mutagen.File(file_path, easy=True)
        meta.add_tags()
    meta['title'] = __get_current_time("month")+"_kimSooHyun"
    meta['artist'] = "201402329"
    meta['genre'] = __get_date_from_file(file_path, "genre")+"_RADIO"
    meta['album'] = __get_date_from_file(file_path, "genre")
    meta.save()

def execute():
    """
    rtmp와 mpc를 실행하는 부분
    """
    rtmp()
    mpc()


def main():
    execute()
main()
