from abc import ABC, abstractmethod

from paddleocr import TextRecognition
from numpy import ndarray
from paddlex.inference.models.text_recognition.result import TextRecResult
from typing import List


class OcrInference(ABC):

    @abstractmethod
    def predict(self, image, output_dir: str):
        pass


class PaddleOCR(OcrInference):

    def __init__(self, model: str) -> None:
        self.model = TextRecognition(model_name=model)

    def predict(self, image: List[ndarray], output_dir: str) -> List[TextRecResult]:
        output = self.model.predict(input=image, batch_size=1)

        for res in output:
            res.print()
            #res.save_to_json(save_path=output_dir + "/res.json")

        return output


def apply_ocr(ocr: OcrInference, image: List[ndarray], output_dir: str) -> List[TextRecResult]:
    return ocr.predict(image, output_dir)
