from awscrt import mqtt
from awsiot import mqtt_connection_builder

import os
from dotenv import load_dotenv

load_dotenv()

ENDPOINT = os.getenv("ENDPOINT")
CLIENT_ID = os.getenv("CLIENT_ID")
CERT_PATH = os.getenv("CERT_PATH")
KEY_PATH = os.getenv("KEY_PATH")
CA_PATH = os.getenv("CA_PATH")
TOPIC = os.getenv("TOPIC")


print("Connecting to AWS IoT...")
mqtt_connection = mqtt_connection_builder.mtls_from_path(
    endpoint=ENDPOINT,
    cert_filepath=CERT_PATH,
    pri_key_filepath=KEY_PATH,
    ca_filepath=CA_PATH,
    client_id=CLIENT_ID,
    clean_session=False,
    keep_alive_secs=30,
)
