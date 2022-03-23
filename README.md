#Flowey - Plant monitoring system with telegram chat and web interface
###IOT project for UNIMORE

##Who is Flowey?
Flowey is the buddy you need to keep your plants alive! Ever wondered how to talk to a plant? Flowey gives you the opportunity!
Just set up the sensors in the vase and start communicating with your plant through Telegram, or access all the data trough the website.
No more guessing if the plant needs water, if it's too cold or if it needs to be placed in another spot. Flowey will tell you if everything it's okay or if it needs some adjustments.

##About the Project
Flowey is part of the project for the exam "Informatica Industriale e IOT" for the Computer Engineering degree in UNIMORE.
We are a team of 3 people who can't seem to keep one single plant alive, not even a cactus, and we decided to invent a system to help us in our "leafy" journey.
The idea is to extend the IOT paradigm to an object which can be found in many households, our plants.

##How does it work
Flowey's systems is composed of various sensors that can be mounted directly on your plant's vase,to monitor humidity, temperature and luminosity, giving a well rounded idea of the plant well being.The data read by the sensors is collected by an Arduino and sent to a RaspberryPi that serves as the bridge using a Serial connection.
While developing we only used one Arduino and one RaspberryPi but there is no real limit to the number of bridges and gateways, since the system is scalable.
The bridge does some elaboration on the data and then sends everything to the Datacenter, that stores the data in MySQL database, hosted on PythonAnywhere.
Flask is installed on our local pc and is used as datacenter. It hosts the REST API (used to connect to telegram and to the database) and the grafic interface to dispay the data through graphs.



For more information about the project read the whole document here (only in italian) --> https://docs.google.com/document/d/1NNB9fvqPyqg2SD_VwvQb1ESI88l5bCgdshtuKrfREr8/edit?usp=sharing

