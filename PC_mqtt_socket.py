# This is the Subscriber
import paho.mqtt.client as mqtt
import threading
import json
import socket
#Don't forget to install "sudo apt-get install -y mosquitto mosquitto-clients"

conf_file = open('IP_configuration.json')
strip_configuration = json.load(conf_file)

class PC_mqtt_socket(threading.Thread):
    cosmoguirlande=mqtt.Client()
    ip_mac = []

    def __init__(self, ip):
        threading.Thread.__init__(self)
        self.data_rcv = ""
        self.ip = ip

    def on_connect(self, mqttc, mosq, obj,rc):
        print("Connected with result code "+str(rc))
        self.cosmoguirlande.subscribe("test1")

    def on_message(self, client, userdata, msg):
        x = msg.payload.decode('utf-8')
        print(str(x))
        self.data_rcv = x
        print("self.data_rcv: ", self.data_rcv)
        #____________________________________________________________________code test here for mac adress sending

        if self.data_rcv.startswith("ip"):
            ip_text, ip, mac_text, mac = self.data_rcv.split(',')
            print("ip: ", ip)
            print("mac: ", mac)

            #Receive Mac Address
            #ip_mac = 

        #____________________________________________________________________end test

    def on_subscribe(self, mosq, obj, mid, granted_qos):
        print("Subscribed: " + str(mid) + " " + str(granted_qos))

    def run(self):
        # Assign event callbacks
        self.cosmoguirlande.on_connect = self.on_connect
        self.cosmoguirlande.on_message = self.on_message
        self.cosmoguirlande.on_subscribe = self.on_subscribe
        self.cosmoguirlande.connect(self.ip, 1883,60)
        print("PC mqtt socket entering in loop forever mode, ip =", self.ip)
        self.cosmoguirlande.loop_forever()

        #self.cosmoguirlande.connect("192.168.1.19",1883,60)
        #self.cosmoguirlande.loop_forever()

        """i = 0

        for elt in strip_configuration["guirlande"]:
            #get IPs from JSON
            print("IP : ", elt["IP"])
            objs = [mqtt.Client() for i in range(len(strip_configuration['guirlande']))]        

            try:
                objs[i].connect(elt["IP"],1883,60)
                print("publish getMacAdress")
                objs[i].publish('test1', "getMacAdress," + socket.gethostbyname(socket.gethostname()))
                objs[i].loop_forever()
                #objs[i].loop_start()

            except:
                print("could not connect to :  ", elt["IP"])
            i = i+1
            """

if __name__ == '__main__':
    
    newSocket_mqtt = PC_mqtt_socket()
    newSocket_mqtt.start()
