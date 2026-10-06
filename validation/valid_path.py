from pathlib import Path
from validation.validation import IValidation


class ValidPath(IValidation):
    extensions = {".jpg", ".jpeg", ".png"}

    def validation(self, source_path: str):
        source = Path(source_path)

        if source.is_file():
            if source.suffix.lower() not in self.extensions:
                raise ValueError(f"Arquivo não suportado: {source}")

            yield source
            return

        elif source.is_dir():
            for file in source.iterdir():
                if file.is_file() and file.suffix.lower() in self.extensions:
                    yield file
            return

        raise ValueError(f"Caminho não encontrado: {source}")
