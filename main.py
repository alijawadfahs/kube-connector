# main.py
import uvicorn
import argparse
import src.database.db as database
import logging

logging.basicConfig(filename='kube-connector.log',
					format='%(asctime)s - %(filename)s:%(lineno)s - %(levelname)s - %(message)s',
					encoding='utf-8',
					level=logging.DEBUG)

def parseCliOptions():

	parser = argparse.ArgumentParser()

	parser.add_argument( '-p', '--port',
		dest       = 'port',
		nargs      = '?',
		type       = int,
		default    = 5000,
		help       = 'The port of the API',
	)
	parser.add_argument( '-k', '--key',
		dest       = 'key',
		nargs      = '?',
		type       = str,
		help       = "encryption key",
	)

	options        = parser.parse_args()
	return options.__dict__

async def app(scope, receive, send):
	...

if __name__ == "__main__":
	logging.info("kube-connector started")
	options = parseCliOptions()
	port    = options["port"]
	key		= options["key"]
	database.create_database()
	uvicorn.run("src.api.api:app", port=port, log_level="info",host="0.0.0.0")