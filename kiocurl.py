#!/usr/bin/env python3
import pycurl
import logging
import tempfile
HOST='10.100.50.104'

def test_curl(url,timeout):
    '''
    Tests if host responds to http req.
    Returns Bool
    '''
    #buffer = BytesIO()
    buffer = tempfile.TemporaryFile()
    val=False
    conn = pycurl.Curl()
    conn.setopt(conn.URL,url)
    conn.setopt(conn.CONNECTTIMEOUT,timeout)
    conn.setopt(conn.HEADER, 1)
    conn.setopt(conn.NOBODY, 1)
    conn.setopt(conn.HEADERFUNCTION, buffer.write)
    conn.setopt(pycurl.WRITEFUNCTION, lambda bytes: len(bytes))
    try:
        conn.perform()
        val=True
    except pycurl.error as e:
        logging.error(e)
    finally:
        conn.close()
        buffer.close()
    return(val)

def get_report(url,timeout):
    '''
    Gets report and headers using cURL
    Returns status and fileobj (200 = Ok)
    '''
    buffer = tempfile.NamedTemporaryFile(prefix='kio_',suffix='.pdf', delete=False,)
    status = 0
    def header_function(header_line):
        nonlocal status
        header_line = header_line.decode('utf-8').strip()
        if 'HTTP/1.1 200 OK' in header_line:
            status=200
        elif 'HTTP/1.1 403 Forbidden' in header_line:
            status=403
        elif 'HTTP/1.1 404 Not_Found' in header_line:
            status=404
    conn = pycurl.Curl()
    conn.setopt(conn.URL, url)
    conn.setopt(conn.CONNECTTIMEOUT,timeout)
    conn.setopt(conn.WRITEFUNCTION, buffer.write)
    # Set our header function.
    conn.setopt(conn.HEADERFUNCTION, header_function)
    try:
        conn.perform()
    except pycurl.error as e:
        logging.error(e)
    finally:
        conn.close()
    return(status, buffer.name)

def main():
    #url='http://10.100.50.104'
    url='http://100.100.50.104'

    #url='http://10.100.50.104/csp/sarmite/ea.kiosk.pdf.cls?HASH=22339362#8534&LANG=RUS'
    #url='http://10.100.50.104/csp/sarmite/ea.kiosk.pdf.cls?HASH=13621914%238444&LANG=RUS'
    f = get_report(url,10)
    print(f[0],f[1].name)
    #f.seek(0,os.SEEK_END)
    #print(f.tell())
if __name__== '__main__':
    logging.basicConfig(format='%(asctime)s - %(message)s',level=logging.DEBUG)
    main()