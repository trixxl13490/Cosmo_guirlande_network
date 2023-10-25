# This is the Subscriber
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("topic/test1")

def on_message(client, userdata, msg):
    if msg.payload.decode() == "Hello world!":
        print("Yes!")

client=mqtt.Client()
client.connect("192.168.0.26",1884,60)

client.on_connect = on_connect
client.on_message = on_message

client.loop_forever()

# This is the Publisher
import paho.mqtt.client as mqtt

client = mqtt.Client()
client.connect("localhost",1884,60)
client.publish("topic/test1", "Hello world!");
