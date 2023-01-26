#!/usr/bin/env python3
import argparse
import logging
from time import sleep, time
import os,re
import gpiolib,bclib,kioconfig,kioprinter
import kiocurl
#from time import sleep

def init_kiosk():
    '''
    Tests pheriferials for kiosk op
    '''
    #Init panel
    global buttonsObj, ledsObj, bcrObj, prnObj, wdObj
    
    #Init Watchdog
    if config['watchdog_device'] is not None:
        try:
            wdObj=open(config['watchdog_device'],'w')
            logging.info('Watchdog enabled on {}'.format(config['watchdog_device']))
        except Exception as e:
            logging.error(e)
    else:
        logging.info('Watchdog disabled')
    
    #Init pheriperials
    buttonsObj  = gpiolib.kioskButtons(pins=config['button_pins'],default=config['default_button'],timeout=config['button_timeout'])
    ledsObj = gpiolib.kioskPWMLeds(pins=config['led_pins'])
    bcrObj=bclib.barCodeReader(port=config['bc_reader_port'], timeout = config['bc_timeout'],)
    prnObj = kioprinter.kioPrinter(config['printers'],testpage=True)
    #Check panel leds
    ledsObj.on()
    buttonsObj.beep(background=False)
    sleep(config['delay'])

    #Init barcode reader, do not start kiosk while bcr not running
    ledsObj.pulse([2],fade_in_time=.1,fade_out_time=.1,n=None)
    logging.info('Starting BC reader on {}'.format(config['bc_reader_port']))
    bcrObj.start()
    while not bcrObj.running:
        sleep(config['delay'])
        bcrObj.start()
    logging.info('BC reader on {} timeout {}'.format(config['bc_reader_port'],config['bc_timeout']))
    #Indicate bc OK
    ledsObj.off([2])
    sleep(config['delay'])

    #Init printer, check if avilable, do not start kiosk while bcr not running
    ledsObj.pulse([1],fade_in_time=.1,fade_out_time=.1,n=None)
    prnObj.start()
    #Reset printsystem if reset button is pressed
    if (buttonsObj.pressed() and buttonsObj.pressedButtons == [1]):
        logging.info('User printsystem reset initiated')
        prnObj.deleteAllPrinters()
        prnObj.installKioPrinter()
        buttonsObj.beep(background=False,n=3)

    while not prnObj.running:
        prnObj.start()
        sleep(config['delay'])
    logging.info('Printer {} on CUPS'.format(prnObj.name))
    #Indicate printer OK
    ledsObj.off([1])
    sleep(config['delay'])

    #Checking if host anewers to cURL requests
    ledsObj.pulse([0],fade_in_time=.1,fade_out_time=.1,n=None)
    test_url = 'http://{}'.format(config['host'])
    status = fname = None
    while not status == 403:
        status,fname = kiocurl.get_report(test_url,config['curl_timeout'])
        #delete cURL temp  file
        try:
            os.remove(fname)
        except FileNotFoundError:
            pass
        logging.info('Host {} responding {}'.format(config['host'],status))
        #Indicate cURL OK
        sleep(config['delay'])
        ledsObj.off()

def make_URL(bar_code):
    '''
    Returns url for cURL request
    '''
    #Remove bc type prefix if present
    if not bar_code[0].isnumeric():
        bar_code=bar_code[1:]
    req_code = re.search(config['bc_regex'],bar_code)
    if req_code is not None:
        req_code = req_code.group(0)
        req_code=req_code.replace('#','%23')
        return(config['url'].format(config['host'],req_code,lang))
    return(None)

def main():
    run_directory = os.path.dirname(os.path.realpath(__file__))
    parser = argparse.ArgumentParser(description='Find duplicate scans')
    parser.add_argument('-c','--config',
                        type=str,
                        metavar='file',
                        help='Name config file. Default: config.ini',
                        default='{}/kiosk.ini'.format(run_directory)
                        )
    args = parser.parse_args()
    #Read from config file
    global config
    config = kioconfig.read_config(args.config)
    if config['log_file'] is None:
        logging.basicConfig(format='%(asctime)s - %(message)s',level=logging.DEBUG)
    else:
        logging.basicConfig(format='%(asctime)s - %(message)s',filename=config['log_file'],filemode='w',level=logging.INFO)
    #Initialize pheripherials
    init_kiosk()
    #Set default language
    lang=config['languages'][config['default_button']]
    #Do not block repeated printing at startup
    ledsObj.off()
    if config['button_panel']:
        ledsObj.blink(leds=[buttonsObj.activeButton],n=None,on_time=config['led_on_time'],off_time=config['led_off_time'],
            fade_in_time=config['led_fade_in'],fade_out_time=config['led_fade_out'])
    logging.info('Main loop started')
    #Main loop+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    while bcrObj.running:
        #Pat watchdog
        if wdObj is not None:
            print('1',file = wdObj, flush = True)
        #Check if panel is enabled, button is pressed or timed-out
        if config['button_panel'] and buttonsObj.pressed():
            #Allow LED driver threads to finish
            sleep(.5)
            ledsObj.off()
            ledsObj.blink(leds=[buttonsObj.activeButton],n=None,on_time=config['led_on_time'],off_time=config['led_off_time'],
                fade_in_time=config['led_fade_in'],fade_out_time=config['led_fade_out'])
            lang=config['languages'][buttonsObj.activeButton]
            logging.debug('{} selected'.format(lang))
        #Barcode
        bc = bcrObj.next()
        if len(bc)==0:
            #Nothing scanned - loop
            #print(".")
            continue
        #Prevent repeated scanning while printing previous report
        logging.debug('Printing {},{}'.format(lang,bc))
        ledsObj.blink(on_time=.2,off_time=.2,fade_in_time=.1,fade_out_time=.1,n=None)
        sleep(5)
        logging.debug('Finished {},{}'.format(lang,bc))
        #Flush buffer
        bcrObj.next()





if __name__=='__main__':
    try:
        wdObj = None
        main()
    except KeyboardInterrupt:
        if wdObj is not None:
            print('V',file = wdObj, flush = True)
        print("\nExiting")
