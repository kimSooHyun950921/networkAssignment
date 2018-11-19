rtmpdump -r "rtmp://new_iradio.ebs.co.kr/iradio/iradiolive_m4a" -B 60 -o EBSResult.flv
ffmpeg -i EBSResult.flv -acodec mp3 EBS1.mp3

mplayer $(curl -s "http://onair.kbs.co.kr/index.html?sname=onair&stype=live&ch_code=24&ch_type=radioList" | grep service_url | tail -1 | cut -d\" -f16 | cut -d\\ -f1) -ao pcm:file=KBS.mp3 -vc dummy -vo null
