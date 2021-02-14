# Paho-mqtt-based-multithreaded-sever-and-edge-application

## Dependencies

1)python3

2)pipenv




## Description

The edge.py app reads simulated data(from "data.csv" file) , converts it into json and publishes to hivemq public broker

The server.py app subscribes to the topic specified , reads the json data and writes it into a file named "result.csv"

The edge.py program has two threads


->producer : which publishes the data at regular interval(specified by programmer), and in case of error pushes the data into a shared queue

->consumer : which in every specified time interval looks for unsend data in shared queue and publishes it too










## Follow the steps for running the application


1)install pipenv 
  
  #sudo apt install pipenv


2)clone the repo in your local folder
  
  #git clone https://github.com/sshri131/Paho-mqtt-based-multithreaded-sever-and-edge-application.git


3)install the dependencies required for the project by typing the  command below in the folder path where project is cloned
  
  #pipenv install --deploy
  

4)run both server.py and edge.py programs in seperated terminal windows

  
