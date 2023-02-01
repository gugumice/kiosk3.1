#!/usr/bin/env python3
#for f in *.mp3 ; do ffmpeg -i "$f"  "${f%.*}.wav" ; done
from subprocess import check_output
import os
from time import sleep
def speak_ip(ip,lang,dir=''):
    #'10'.replace('.')
    for char in ip:
        f = ('{}/{}_{}.wav'.format(dir,char.replace('.','dot'),lang.upper()))
        try:
            os.system('aplay -q {} 2>&1'.format(f))
            #sleep(1)
        except Exception as e:
            pass

def get_IP():
    try:
        ip = check_output(['hostname', '-I']).decode('utf-8')
        return(ip.strip())
    except:
        return(None)
def speak_status(f):
    try:
        os.popen('aplay -q {} 2>&1'.format(f))
    except:
        pass

def main():
    dir = (os.path.dirname(os.path.realpath(__file__)))
    print(get_IP())
    speak_ip(ip=get_IP(),lang='lat',dir=dir)
    speak_status('{}/{}ready.wav'.format(dir,'ready_LV'))
    print('{}/{}.wav'.format(dir,'ready_LV'))


if __name__ == '__main__':
    main()