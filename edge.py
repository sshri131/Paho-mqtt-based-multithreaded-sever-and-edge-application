import threading
import time
import random
import queue
import csv
import json
import paho.mqtt.client as mqtt

BUF_SIZE = 10
q = queue.Queue(BUF_SIZE)
broker_addr = "broker.hivemq.com"
port = 1883 
keepalive = 60
temperatureTopic="sensor/sensor_sshri131"

sentMessages = 0

class ProducerThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        super(ProducerThread,self).__init__()
        self.target = target
        self.name = name

    def run(self):
        willTopic="sensor/issues"
        willPayload = "Sensor stops sending the data"
        client = mqtt.Client(client_id="mainClient", clean_session=True, transport="tcp")
        client.will_set(willTopic, willPayload, qos=1, retain=False)
        global sentMessages
        
        #connect to Broker
        client.connect(broker_addr,port,keepalive)
        print("producer connected")
        while True:
            with open("dataset.csv") as file:
                next(file) #skip the header
                reader = csv.reader(file)
                for row in reader:
                    temp = dict(timestamp = row[0],temp = row[1])
                    payload = json.dumps(temp)
                    errorFlag = random.choice([0,1]) #simulating error
                    if(errorFlag == 0):
                        if not q.full():
                            q.put(payload)
                    else:
                        client.publish(temperatureTopic,payload)
                        sentMessages += 1


                    time.sleep(60)
            return

class ConsumerThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        super(ConsumerThread,self).__init__()
        self.target = target
        self.name = name
        return

    def run(self):
        client = mqtt.Client(client_id="backupClient", clean_session=True, transport="tcp")
        client.connect(broker_addr,port,keepalive)
        global sentMessages
        print("consumer connected")
        while True:
            while not q.empty():
                payload = q.get()
                client.publish(temperatureTopic,payload)
                sentMessages += 1
            time.sleep(5)
        return

#function to get the count of buffered data chunks at any point in time.
def bufferedMessagesCount(self):
    return q.qsize()

#function to get the count of successfully transmitted data chunks at any point in time.
def sentMessageCount(self):
    return sentMessages

if __name__ == '__main__':
    p = ProducerThread(name='producer')
    c = ConsumerThread(name='consumer')

    p.start()
    c.start()
