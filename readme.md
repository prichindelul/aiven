~~~~AIVEN Test~~~~
- To install the libraries I used, run the install.bat file first. You must have PIP installed on your machine.
- You need to create the topic "test1" on the Kafka machine.
- To start the producer, you need to start it with the following command:
	py producer.py URL REGEX
	
		- where URL is the url of the webpage you want to check 
		- where REGEX is the regular expression you want to check in the page body of the webpage you want to check.