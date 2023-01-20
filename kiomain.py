#!/usr/bin/env python3
import argparse
import logging
import gpiolib,bclib,kioconfig,kioprinter
#from time import sleep

def init_kiosk():
    '''
    Tests pheriferials for kiosk op
    '''
    #Init panel
    global buttonsObj, ledsObj, bcrObj, prnObj
    buttonsObj  = gpiolib.kioskButtons(config['button_pins'])
    ledsObj = gpiolib.kioskPWMLeds(config['led_pins'])
    bcrObj=bclib.barCodeReader(port=config['bc_reader_port'], timeout =config['bc_timeout'])
    prnObj = kioprinter.kioPrinter(config['printers'],testpage=True)
    ledsObj.on()
    buttonsObj.beep(background=False)
    print(config)
    
def main():
    parser = argparse.ArgumentParser(description='Find duplicate scans')
    parser.add_argument('-c','--config',
                        type=str,
                        metavar='file',
                        help='Name config file. Default: config.ini',
                        default='kiosk3/kiosk.ini'
                        )
    args = parser.parse_args()
    #Read from config file
    global config
    config = kioconfig.read_config(args.config)

    if config['log_file'] is None:
        logging.basicConfig(format='%(asctime)s - %(message)s',level=logging.DEBUG)
    else:
        logging.basicConfig(format='%(asctime)s - %(message)s',filename=config['log_file'],filemode='w',level=logging.INFO)
    init_kiosk()

if __name__=='__main__':
    try:
        wdObj = None
        main()
    except KeyboardInterrupt:
        if wdObj is not None:
            print('V',file = wdObj, flush = True)
        print("\nExiting")
