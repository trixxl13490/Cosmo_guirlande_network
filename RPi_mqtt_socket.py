# This is the Subscriber
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("test1")

def on_message(client, userdata, msg):
    print(str(msg))

cosmoguirlande_1=mqtt.Client()
cosmoguirlande_1.connect("localhost",1883,60)
cosmoguirlande_1.on_connect = on_connect
cosmoguirlande_1.on_message = on_message

cosmoguirlande_2=mqtt.Client()
cosmoguirlande_2.connect("192.168.0.20",40002,60)
cosmoguirlande_2.on_connect = on_connect
cosmoguirlande_2.on_message = on_message

cosmoguirlande_3=mqtt.Client()
cosmoguirlande_3.connect("192.168.0.20",40003,60)
cosmoguirlande_3.on_connect = on_connect
cosmoguirlande_3.on_message = on_message

cosmoguirlande_4=mqtt.Client()
cosmoguirlande_4.connect("192.168.0.20",40004,60)
cosmoguirlande_4.on_connect = on_connect
cosmoguirlande_4.on_message = on_message

cosmoguirlande_5=mqtt.Client()
cosmoguirlande_5.connect("192.168.0.20",40005,60)
cosmoguirlande_5.on_connect = on_connect
cosmoguirlande_5.on_message = on_message

cosmoguirlande_6=mqtt.Client()
cosmoguirlande_6.connect("192.168.0.20",40006,60)
cosmoguirlande_6.on_connect = on_connect
cosmoguirlande_6.on_message = on_message

cosmoguirlande_7=mqtt.Client()
cosmoguirlande_7.connect("192.168.0.20",40007,60)
cosmoguirlande_7.on_connect = on_connect
cosmoguirlande_7.on_message = on_message



cosmoguirlande_1.loop_forever()
cosmoguirlande_2.loop_forever()
cosmoguirlande_3.loop_forever()
cosmoguirlande_4.loop_forever()
cosmoguirlande_5.loop_forever()
cosmoguirlande_6.loop_forever()
cosmoguirlande_7.loop_forever()
