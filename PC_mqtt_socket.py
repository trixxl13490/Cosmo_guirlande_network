# This is the Publisher - from PC or tablet
import paho.mqtt.client as mqtt

cosmoguirlande_1 = mqtt.Client()
cosmoguirlande_2 = mqtt.Client()
cosmoguirlande_3 = mqtt.Client()
cosmoguirlande_4 = mqtt.Client()
cosmoguirlande_5 = mqtt.Client()
cosmoguirlande_6 = mqtt.Client()
cosmoguirlande_7 = mqtt.Client()

cosmoguirlande_1.connect("192.168.1.53",1883, 60)
cosmoguirlande_1.publish("test1", "cosmoguirlande,Sinelon");

cosmoguirlande_2.connect("192.168.0.36",1883,60)
cosmoguirlande_2.publish("test1", "Hello world!");

cosmoguirlande_3.connect("192.168.0.7",1883,60)
cosmoguirlande_3.publish("test1", "Hello world!");

cosmoguirlande_4.connect("192.168.0.5",1883,60)
cosmoguirlande_4.publish("test1", "Hello world!");

