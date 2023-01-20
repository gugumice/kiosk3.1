#!/usr/bin/env python3
import configparser
import logging
import json
import os

def read_config(filename):
    kiosk_config = {
        'log_file': None,
        'button_panel': False,
        'button_pins': [17,27,22],
        'led_pins': [13,19,26],
        'buzzer_pin': 12,
        'default_button' : 0,
        'button_timeout' : 10,
        'melody': ["C4","A4","C4"],
        'sound_interval': .12,
        'languages' : ['LAT','ENG','RUS'],
        'delay':2,

        'bc_reader_port' : '/dev/ttyACM0',
        'bc_timeout' : 1,
        'bc_regex' : '^\d{7,9}#\d{4,5}',

        'host' : '10.100.50.104',
        'curl_timeout': 15, 
        'report_delay' : 5,
        'url' : 'http://{}/csp/sarmite/ea.kiosk.pdf.cls?HASH={}&LANG={}',
        'printers':  {"HP": "HP LaserJet Series PCL 6 CUPS"},
        'button_printer_reset' : [1],
        'wd' : '/dev/watchdog'
    }
    if not os.path.isfile(filename):
        logging.critical("Config file {} does not exist!".format(filename))
        return(None)
    cf = configparser.ConfigParser(allow_no_value=True,
                            converters={'list': lambda x: [int(i.strip()) for i in x.split(',')],
                                        'list_s' : lambda x: [i.strip() for i in x.split(',')]})
    cf.read(filename)
    try:
        kiosk_config['log_file'] = cf.get('IFACE','log_file')
        kiosk_config['button_panel'] = cf.getboolean('IFACE','button_panel')
        kiosk_config['button_pins'] = cf.getlist('IFACE','button_pins')
        kiosk_config['led_pins'] = cf.getlist('IFACE','led_pins')
        kiosk_config['buzzer_pin'] = cf.getint('IFACE','buzzer_pin')
        kiosk_config['default_button'] = cf.getint('IFACE','default_button')
        kiosk_config['button_timeout'] = cf.getint('IFACE','button_timeout')
        kiosk_config['melody'] = cf.getlist_s('IFACE','melody')
        kiosk_config['sound_interval'] = cf.getfloat('IFACE','sound_interval')
        kiosk_config['languages'] = cf.getlist_s('IFACE','languages')
        kiosk_config['delay'] = cf.getfloat('IFACE','delay')

        kiosk_config['bc_reader_port'] = cf.get('BARCODE','bc_reader_port')
        kiosk_config['bc_timeout'] = cf.getint('BARCODE','bc_timeout')
        kiosk_config['bc_regex'] = r'{}'.format(cf.get('BARCODE','bc_regex'))

        kiosk_config['host'] = cf.get('REPORT','host')  
        kiosk_config['curl_timeout'] = cf.getint('REPORT','curl_timeout')
        kiosk_config['report_delay'] = cf.getint('REPORT','report_delay')
        kiosk_config['url'] = cf.get('REPORT','url')
        kiosk_config['button_printer_reset'] = cf.getlist('REPORT','button_printer_reset')
        kiosk_config['printers'] = json.loads(cf.get('REPORT','printers'))
        kiosk_config['watchdog_device'] = cf.get('WATCHDOG','watchdog_device')
    except configparser.Error as e:
        logging.error(e)
   
    return(kiosk_config)

def main():
    f = '{}/{}'.format(os.getcwd(),'kiosk.ini')
    cfg = read_config(f)
    print(cfg)
    print(list(cfg['printers'].keys())[0])

if __name__ == '__main__':
    main()
