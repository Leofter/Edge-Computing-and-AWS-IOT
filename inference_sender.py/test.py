from awscrt import mqtt
from awsiot import mqtt_connection_builder
import time

import os
from dotenv import load_dotenv

load_dotenv()

ENDPOINT = os.getenv("ENDPOINT")
CLIENT_ID = os.getenv("CLIENT_ID")
CERT_PATH = os.getenv("CERT_PATH")
KEY_PATH = os.getenv("KEY_PATH")
CA_PATH = os.getenv("CA_PATH")
TOPIC = os.getenv("TOPIC")

# Connect
print("Connecting to AWS IoT Core...")
mqtt_connection = mqtt_connection_builder.mtls_from_path(
    endpoint=ENDPOINT,
    cert_filepath=CERT_PATH,
    pri_key_filepath=KEY_PATH,
    ca_filepath=CA_PATH,
    client_id=CLIENT_ID,
    clean_session=False,
    keep_alive_secs=30,
)

mqtt_connection.connect().result()
print("Connected successfully!")

# Send a test message
import json

test_message = {
    "device_id": CLIENT_ID,
    "message": "Hello from VSCode!",
    "timestamp": int(time.time()),
}

mqtt_connection.publish(
    topic=TOPIC, payload=json.dumps(test_message), qos=mqtt.QoS.AT_LEAST_ONCE
)
print(f"Test message sent: {test_message}")

# Disconnect
mqtt_connection.disconnect().result()
print("Done!")
