'''
Created on 13.05.2021

@author: Mircea
'''
#consumer
#https://towardsdatascience.com/using-kafka-for-collecting-web-application-metrics-in-your-cloud-data-lake-b97004b2ce31
# This script receives messages from a Kafka topic
import time
import threading
import datetime
from kafka import KafkaConsumer
from create_table import create_table
from insert_logs import insert_log
consumer = KafkaConsumer(
    "test1",
    auto_offset_reset="earliest",
    bootstrap_servers="kafka-16dcc46d-florian-f653.aivencloud.com:25606",
    client_id="demo-client-1",
    group_id="demo-group",
    security_protocol="SSL",
    ssl_cafile="ca.pem",
    ssl_certfile="service.cert",
    ssl_keyfile="service.key",    
    enable_auto_commit=True,
    auto_commit_interval_ms=1000,
    consumer_timeout_ms=-1
)

# Call poll twice. First call will just assign partitions for our
# consumer without actually returning anything
'''
for _ in range(2):
    raw_msgs = consumer.poll(timeout_ms=1000)
    for tp, msgs in raw_msgs.items():
        for msg in msgs:
            print("Received: {}".format(msg.value))

# Commit offsets so we won't get the same messages again

consumer.commit()
'''


def fetch_last_min_requests(next_call_in, is_first_execution=False):
	next_call_in = next_call_in+60
	counter_requests = 0
	if is_first_execution:
		create_table()		
		with open("requests.csv","a") as file:
			headers = ["datetime", "requests_num", "message"]
			file.write(",".join(headers))
			file.write("\n")
	else:
		batch = consumer.poll(timeout_ms=1000)		
		if len(batch) > 0:
			for message in list(batch.values())[0]:
				counter_requests += 1
				with open("requests.csv","a") as file:
					data = [datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(counter_requests), str(message.value)]
					insert_log(str(message.value))
					file.write(",".join(data))
					file.write("\n")
	
	threading.Timer(next_call_in - time.time(),fetch_last_min_requests,[next_call_in]).start()


if __name__ == '__main__':
	next_call_in = time.time()
	fetch_last_min_requests(next_call_in, True)