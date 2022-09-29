# boot.py -- run on boot-up
import time
from umqttsimple import MQTTClient
import network
import esp
import gc

esp.osdebug(None)

gc.collect()

def do_connect():
    ssid = 'REDE'
    password = '123456789' 
    
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(ssid, password)
        #sta_if.connect('REDE', '123456789')
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())

    

do_connect()