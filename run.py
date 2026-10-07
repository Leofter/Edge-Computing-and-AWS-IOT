from awscrt import mqtt
from awsiot import mqtt_connection_builder
import time
import json
import uuid

import os
from dotenv import load_dotenv

from service.pipeline import OCR as ocr
from service.pipeline import ROI as roi
from service.pipeline import detection as dt

from datetime import datetime

from repository.awsRepository import AwsS3
from repository.awsRepository import AwsSNS

from validation.valid_path import ValidPath

from api.dto.ocrResultDto import OCRResultDTO

load_dotenv()


# IOT
ENDPOINT = os.getenv("ENDPOINT")
CLIENT_ID = os.getenv("CLIENT_ID")
CERT_PATH = os.getenv("CERT_PATH")
KEY_PATH = os.getenv("KEY_PATH")
CA_PATH = os.getenv("CA_PATH")
TOPIC = os.getenv("TOPIC")

# S3
S3_BUCKET = os.getenv("S3_BUCKET")

# SNS
SNS_TOPIC = os.getenv("SNS_TOPIC")

# CONFIG YOLO
yolo_model = os.getenv("YOLO_MODEL")
image_path = os.getenv("IMAGE_PATH")  # corrigir para dataset e image
conf = 0.5

# CONFIG OCR
ocr_model = "PP-OCRv6_medium_rec"
ocr_output = "ocr_output"

# init Detection and OCR
detector = dt.YoloDetection(yolo_model)
ocr_init = ocr.PaddleOCR(ocr_model)
Crop_mode = roi.Crop(image_path)

# RUN
detection_result = dt.apply_detection(detector, image_path, conf)

image_roi = roi.apply_roi(Crop_mode, detection_result)

ocr_result = ocr.apply_ocr(ocr_init, image_roi, ocr_output)

# connect s3
s3 = AwsS3()
s3.connect(S3_BUCKET, CLIENT_ID)

# connect sns
sns = AwsSNS()
sns.connect(SNS_TOPIC)

# Connect iot
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
print("Connected iot")


files = list(ValidPath().validation(image_path))


for file, item in zip(files, ocr_result):

    # DTO do OCR
    raw_data = item.get("res", item)
    dto = OCRResultDTO(**raw_data)
    ocr_result_json = dto.model_dump(exclude_none=True)

    # save s3
    inference_id = str(uuid.uuid4())
    s3_uri = s3.upload(inference_id, file)

    # mensagem
    message = {
        "inference_id": inference_id,
        "device_id": CLIENT_ID,
        "timestamp": int(time.time()),
        "s3_uri": s3_uri,
        "ocr_data": ocr_result_json,
        "date_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    mqtt_connection.publish(
        topic=TOPIC, payload=json.dumps(message), qos=mqtt.QoS.AT_LEAST_ONCE
    )
    print(f"Test message sent: {message}")

    sns.publish(True)


mqtt_connection.disconnect().result()
print("Disconnected IOT")
