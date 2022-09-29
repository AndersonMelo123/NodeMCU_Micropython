# from platform import machine
from hcsr04 import HCSR04
import time
from machine import *
from umqttsimple import MQTTClient
import ubinascii

client_id = ubinascii.hexlify(unique_id())
sensor_type = "HC-SR04"
print("ID: ", client_id)

topic_sub = b'notification'
topic_node = b'node'
topic_pub = b'iot'
mqtt_server = '192.168.137.173'

last_message = 0
message_interval = 1
counter = 0

Led = Pin(4, Pin.OUT)

buzzer = PWM(Pin(15), Pin.OUT)

sensor = HCSR04(trigger_pin=13, echo_pin=14, echo_timeout_us=10000)


def sub_cb(topic, msg):
    print((topic, msg))
    if topic == b'notification':
        print('ESP received hello message.')

def connect_and_subscribe():
    global client_id, mqtt_server, topic_sub
    client = MQTTClient(client_id, mqtt_server)
    client.set_callback(sub_cb)
    client.connect()
    client.subscribe(topic_sub)
    print('Connected to %s MQTT broker, subscribed to %s topic' %
          (mqtt_server, topic_sub))
    return client


def restart_and_reconnect():
    print('Failed to connect to MQTT broker. Reconnecting...')
    time.sleep(10)
    machine.reset()


try:
    client = connect_and_subscribe()
except OSError as e:
    restart_and_reconnect()

while True:
    distance = sensor.distance_cm()
    if distance < 50 and distance > 0:
        print(type(distance))
        #dis = 50 - distance
        dados = '{"id":"'+client_id.decode("utf-8") +'", "sensor": "'+sensor_type+'", "data": "'+str(distance)+'"}' 
        print("dados", dados)
        msg = b'%s' % dados
        msg2 = b'%.2f' % distance
        client.publish(topic_pub, msg)
        client.publish(topic_node, msg2)
        Led.value(1)

        buzzer.freq(1047)
        buzzer.duty(512)
        time.sleep(1)
        buzzer.duty(0)
        buzzer.deinit()
        
        Led.value(0)
    
    elif distance > 50:
        x = 0
        dados = '{"id":"'+client_id.decode("utf-8") +'", "sensor": "'+sensor_type+'", "data": "'+str(x)+'"}' 
        msg = b'%s' % dados
        msg2 = b'%d' % x
        client.publish(topic_pub, msg)
        client.publish(topic_node, msg2)

    print('Distance:', distance, 'cm')
    time.sleep(1)