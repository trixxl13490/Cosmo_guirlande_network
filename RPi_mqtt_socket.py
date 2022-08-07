# This is the Subscriber
import paho.mqtt.client as mqtt
import threading
#Don't forget to install "sudo apt-get install -y mosquitto mosquitto-clients"

class RPi_mqtt_socket(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.data_rcv = ""

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        self.client.subscribe("test1")

    def on_message(self, client, userdata, msg):
        print(str(msg))
        self.data_rcv = str(msg)

    cosmoguirlande=mqtt.Client()
    cosmoguirlande.connect("localhost",1883,60)
    cosmoguirlande.on_connect = on_connect
    cosmoguirlande.on_message = on_message
    cosmoguirlande.loop_forever()


