import csv
import json
import paho.mqtt.client as mqtt


broker_addr = "broker.hivemq.com"
port = 1883 
keepalive = 60

temperatureTopic="sensor/sensor_sshri131"
temperatureQos = 0

willTopic="sensor/issues"
willQos = 1



# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(temperatureTopic,temperatureQos)
    print("Subscription to temperature topic added")
    client.subscribe(willTopic,willQos)
    print("Subscription to last will  topic added")
    

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    if(msg.topic == temperatureTopic):
        m_decode=msg.payload.decode()
        payloadDictionary = json.loads(m_decode)

        with open("result.csv","a") as file:
            writer = csv.writer(file)
            writer.writerow(list(payloadDictionary.values()))
    if(msg.topic == willTopic):
        print("disconnected with message : " + msg.payload.decode())


client = mqtt.Client()   
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_addr, port, keepalive)

with open("result.csv" ,  "w") as file:
    writer = csv.writer(file)
    writer.writerow(["timestamp","sensor1"])


client.loop_forever()
