from awscrt import mqtt
from awsiot import mqtt_connection_builder
import time
import json

import os
from dotenv import load_dotenv

from service.pipeline import OCR as ocr
from service.pipeline import ROI as roi
from service.pipeline import detection as dt

from api.dto.ocrResultDto import OCRResultDTO

load_dotenv()

ENDPOINT = os.getenv("ENDPOINT")
CLIENT_ID = os.getenv("CLIENT_ID")
CERT_PATH = os.getenv("CERT_PATH")
KEY_PATH = os.getenv("KEY_PATH")
CA_PATH = os.getenv("CA_PATH")
TOPIC = os.getenv("TOPIC")


# CONFIG YOLO
yolo_model = os.getenv("YOLO_MODEL")
image_path = os.getenv("IMAGE_PATH")
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

for item in ocr_result:
    raw_data = item.get("res", item)

    dto = OCRResultDTO(**raw_data)

    ocr_result_json = dto.model_dump(exclude_none=True)

json.dumps(message)= {
    "device_id": CLIENT_ID,
    "ocr_data": ocr_result_json,
    "timestamp": int(time.time()),
}

