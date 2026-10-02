from abc import ABC, abstractmethod

import numpy as np
from ultralytics import YOLO
from numpy import ndarray
from typing import List, Tuple

DetectionResults = list[tuple[str, np.ndarray]]


class Detection(ABC):

    @abstractmethod
    def predict(self, image_path: str, conf: float) -> DetectionResults:
        pass


class YoloDetection(Detection):

    def __init__(self, model_path: str) -> None:
        self.model = YOLO(model_path)

    def predict(self, image_path: str, conf: float) -> DetectionResults:
        results = self.model.predict(
            source=image_path,
            conf=conf,
        )

        detections = []
        for result in results:
            boxes = result.boxes.xyxy.cpu().numpy()
            detections.append((result.path, boxes))

        return detections


def apply_detection(detection: Detection, image: str, conf: float) -> List[Tuple[str, ndarray]]:
    return detection.predict(image, conf)
