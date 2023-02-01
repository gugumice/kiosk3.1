#!/usr/bin/python3
#for f in *.mp3 ; do ffmpeg -i "$f"  "${f%.*}.wav" ; done
import os
from time import sleep
def read_ip(ip,lang,dir=''):
    #'10'.replace('.')
    for char in ip:
        f = ('{}/{}_{}.wav'.format(dir,char.replace('.','dot'),lang))
        try:
            os.system('aplay -q {} 2>&1'.format(f))

            #sleep(1)
        except Exception as e:
            pass

def main():
    dir = (os.path.dirname(os.path.realpath(__file__)))
    read_ip('10.100.110.223','lv'.upper(),dir)
    sleep(1)
    read_ip('1234567890.ase','lv'.upper(),dir)

if __name__=="__main__":
    main()
