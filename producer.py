'''
Created on 13.05.2021

@author: Mircea
'''
#kafka producer
#https://towardsdatascience.com/using-kafka-for-collecting-web-application-metrics-in-your-cloud-data-lake-b97004b2ce31
from kafka import KafkaProducer
import requests
import time
import threading
import datetime
import re
import sys
import http.client


producer = KafkaProducer(
    bootstrap_servers="kafka-16dcc46d-florian-f653.aivencloud.com:25606",
    security_protocol="SSL",
    ssl_cafile="ca.pem",
    ssl_certfile="service.cert",
    ssl_keyfile="service.key",
)

#Get the Http Status of the URL Request
def getStatus(url, path="/"): 
	try:
		r = requests.get(url)
		return str(r.status_code)
		# prints the int of the status code. Find more at httpstatusrappers.com :)
	except requests.ConnectionError:
		return ("Failed to connect "+str(requests.ConnectionError))


#Get the Http Response Time of the URL Request
def getResponseTime(url):
	try:
		x = requests.get(url)	
		return str(x.elapsed)
	except requests.ConnectionError:
		return ("Failed to connect "+str(requests.ConnectionError))

#Get the Body of the Page from the URL Request
def getPage(url):
	try:
		x = requests.get(url)
		#print(x.content)	
		return str(x.content)
	except requests.ConnectionError:
		return ("Failed to connect "+str(requests.ConnectionError))


#Send message to a Kafka topic
def sendToKafka(topic, message):
	print("Sending: {}".format(message))
	producer.send(topic, message.encode("utf-8"))

#Checks if the regex is valid
def check_regex(regex):
	try:
		re.compile(regex)
		return True
	except re.error:
		return False
		

def check_argumets():
	#check if there is a valid URL which contains http
	if "http" not in sys.argv[1]:
		sys.argv[1]="http://"+sys.argv[1]
		sys.exit("Invalid URL. Perhaps you meant "+sys.argv[1])
	#check if there is a valid webpage
	#if "failed to connect" in getStatus(sys.argv[1]):
	#	sys.exit("Failed to connect "+sys.argv[1]+" "+ str(requests.ConnectionError))
	#check if the REGEX is valid
	if not check_regex(sys.argv[2]):
		sys.exit("The provided regular expression \""+ sys.argv[2] +"\" is not a valid regex. Please enter a valid REGEX")

#Threading function which checks the availability of the url.
def last_min_check(url, regex, next_call_in, is_first_execution=False):
	next_call_in = next_call_in+60
	counter_requests = 0
	topic="test1"
	sendToKafka(topic,"Status Code "+str(url)+": "+ getStatus(url))
	sendToKafka(topic,"Response Time "+str(url)+": " + getResponseTime(url))
	#Search for the regex in the page
	if re.search(regex, getPage(url)):
		sendToKafka(topic,"The regular expression \""+ regex +"\" was found in the page body from "+url)
	else:
		sendToKafka(topic,"The regular expression \""+ regex +"\" was not found in the page body from "+url)	
	# Force sending of all messages
	producer.flush()
	#Check url every 60 seconds
	threading.Timer(next_call_in - time.time(),last_min_check,[url,regex, next_call_in]).start()

if __name__ == '__main__':
	next_call_in = time.time()
	check_argumets()
	print(sys.argv[1])
	last_min_check(str(sys.argv[1]),str(sys.argv[2]), next_call_in, True)