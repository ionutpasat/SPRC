import paho.mqtt.client as mqtt
import time

brokerHost = "127.0.0.1"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("test")

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client("task2")

print("Connecting to broker ", brokerHost)
client.connect(brokerHost, 1883, 60)

client.on_connect = on_connect
client.on_message = on_message

client.loop_start()

client.publish("sprc/chat/Ionut", "Hello World!")
time.sleep(2)

client.loop_stop()
client.disconnect()