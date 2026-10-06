from abc import ABC, abstractmethod


class IValidation(ABC):
    @abstractmethod
    def validation(self, source_path: str):
        pass
