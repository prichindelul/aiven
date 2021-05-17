#Get the Http Status of the URL Request
def getStatus(url): 
	x = requests.get(url)
	return(x.status_code)
	
#Get the Http Response Time of the URL Request
def getResponseTime(url):
	x = requests.get(url)
	return(x.elapsed)

#Get the Body of the Page from the URL Request
def getPage(url):
	x = requests.get(url)
	return(x.content)

#Send message to a Kafka topic
def sendToKafka(topic, message):
	print("Sending: {}".format(message))
	producer.send(topic, message.encode("utf-8"))
	producer.flush()

producer = KafkaProducer(
    bootstrap_servers="kafka-16dcc46d-florian-f653.aivencloud.com:25606",
    security_protocol="SSL",
    ssl_cafile="ca.pem",
    ssl_certfile="service.cert",
    ssl_keyfile="service.key",
)