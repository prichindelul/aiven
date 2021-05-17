~~~~
Aiven Test
- To install the libraries I used, run the install.bat file first. You must have PIP installed on your machine.
- You need to create the topic "test1" on the Kafka machine.
- Make sure you have all of the correct certificates(the certificates of my test machine are in the repository)
- To connect to the PostgreSQL Server machine please update the database.ini file with the correct credentials and host
- To start the **producer**, you need to start it with the following command:
	py producer.py URL REGEX	
		  - where URL is the url of the webpage you want to check 
		  - where REGEX is the regular expression you want to check in the page body of the webpage you want to check.
- To start the **consumer**, you need to start it with the following command:
 	py consumer.py

Note: the **consumer** writes in the PostgreSQL DB and also to a local CSV file
