# This is the Subscriber
import paho.mqtt.client as mqtt
import threading
import json
#Don't forget to install "sudo apt-get install -y mosquitto mosquitto-clients"

class RPi_mqtt_socket(threading.Thread):
    cosmoguirlande=mqtt.Client()

    def __init__(self):
        threading.Thread.__init__(self)
        self.data_rcv = ""

    def on_connect(self, mqttc, mosq, obj,rc):
        print("Connected with result code "+str(rc))
        self.cosmoguirlande.subscribe("test1")

    def on_message(self, client, userdata, msg):
        x = msg.payload.decode('utf-8')
        print(str(msg))
        print(str(x))
        self.data_rcv = str(msg)
        print("self.data_rcv: ", self.data_rcv)

    def on_subscribe(self, mosq, obj, mid, granted_qos):
        print("Subscribed: " + str(mid) + " " + str(granted_qos))

    def run(self):
    # Assign event callbacks
        self.cosmoguirlande.on_connect = self.on_connect
        self.cosmoguirlande.on_message = self.on_message
        self.cosmoguirlande.on_subscribe = self.on_subscribe
        self.cosmoguirlande.connect("localhost",1883,60)
        self.cosmoguirlande.loop_forever()

if __name__ == '__main__':
    
    newSocket_mqtt = RPi_mqtt_socket()
    newSocket_mqtt.start()