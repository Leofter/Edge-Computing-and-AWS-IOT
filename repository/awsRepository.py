from awscrt import mqtt
from awsiot import mqtt_connection_builder

import os
from dotenv import load_dotenv

load_dotenv()


class ConnectAwsIot:
    def __init__(
        self,
        ENDPOINT,
        CERT_PATH,
        KEY_PATH,
        CA_PATH,
        CLIENT_ID,
        clean_session,
        keep_alive_secs,
    ):
        self.endpoint = ENDPOINT
        self.cert_path = CERT_PATH
        self.pri_key_filepath = KEY_PATH
        self.ca_filepath = CA_PATH
        self.client_id = CLIENT_ID
        self.clean_session = clean_session
        self.keep_alive_secs = keep_alive_secs

    def conect(self):
        print("Connecting to AWS IoT...")
        self.mqtt_connection = mqtt_connection_builder.mtls_from_path(
            endpoint=self.endpoint,
            cert_filepath=self.cert_path,
            pri_key_filepath=self.pri_key_filepath,
            ca_filepath=self.ca_filepath,
            client_id=self.client_id,
            clean_session=self.clean_session,
            keep_alive_secs=self.keep_alive_secs,
        )

        self.mqtt_connection.connect().result()
        print("Connected")

    def disconnect(self):
        self.mqtt_connection.disconnect().result()
        print("Disconnected")

    def publish(self, messege, topic):
        self.mqtt_connection.publish(
            topic=topic, payload=messege, qos=mqtt.QoS.AT_LEAST_ONCE
        )
