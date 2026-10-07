from awscrt import mqtt
from awsiot import mqtt_connection_builder
import boto3
import json

from abc import ABC, abstractmethod
from datetime import datetime, timezone
from os import PathLike


class ConnectAws(ABC):

    @abstractmethod
    def connect(self):
        pass


class ConnectAwsIot(ConnectAws):
    def __init__(
        self,
        endpoint,
        cert_path,
        key_path,
        ca_path,
        client_id,
        clean_session,
        keep_alive_secs,
    ):
        self.endpoint = endpoint
        self.cert_path = cert_path
        self.pri_key_filepath = key_path
        self.ca_filepath = ca_path
        self.client_id = client_id
        self.clean_session = clean_session
        self.keep_alive_secs = keep_alive_secs

    def connect(self):
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


class AwsS3:

    def connect(self, bucket_name, client_id):
        self.client_id = client_id
        self.s3 = boto3.resource("s3")
        self.bucket = self.s3.Bucket(bucket_name)
        self.bucket_name = bucket_name

    def upload(self, inference_id: str, image_path: str | PathLike[str]) -> str:
        now = datetime.now(timezone.utc)

        s3_key = f"inference-image/{self.client_id}/{now:%Y/%m/%d}/{inference_id}.jpg"

        self.bucket.upload_file(
            Filename=image_path,
            Key=s3_key,
            ExtraArgs={
                "ContentType": "image/jpeg",
                "Metadata": {"inference_id": inference_id, "device_id": self.client_id},
            },
        )

        return f"s3://{self.bucket_name}/{s3_key}"


class AwsSNS:

    def connect(self, sns_topic):
        self.sns = boto3.resource("sns", region_name="us-east-2")
        self.topic = self.sns.Topic(sns_topic)
        self.sns_topic = sns_topic

    def publish(self, alerta: bool) -> str:
        # self.id_ocr = id_ocr -> futuramente adicionar

        if alerta == True:

            mensage = {
                "tipo": "ALERTA",
                "motivo": f"Desconformidade",
            }

            self.topic.publish(
                Subject="Alerta de Desconformidade",
                Message=json.dumps(mensage, ensure_ascii=False, indent=2),
            )
            print(f"[SNS]: Alerta enviado")
            return
