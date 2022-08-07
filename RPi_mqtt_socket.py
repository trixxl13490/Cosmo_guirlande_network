# This is the Subscriber
import paho.mqtt.client as mqtt
import threading
#Don't forget to install "sudo apt-get install -y mosquitto mosquitto-clients"

class RPi_mqtt_socket(threading.Thread):
    cosmoguirlande=mqtt.Client()

    def __init__(self):
        threading.Thread.__init__(self)
        self.data_rcv = ""

    def on_connect(self, mqttc, mosq, obj,rc):
        print("Connected with result code "+str(rc))
        self.subscribe("test1")

    def on_message(self, client, userdata, msg):
        print(str(msg))
        self.data_rcv = str(msg)

    def run(self):
    # Assign event callbacks
        self.cosmoguirlande.on_connect = self.on_connect.connect("localhost",1883,60)
        self.cosmoguirlande.on_message = self.on_message
        self.cosmoguirlande.on_publish = self.on_publish
        self.cosmoguirlande.on_subscribe = self.on_subscribe
        self.cosmoguirlande.loop_forever()

