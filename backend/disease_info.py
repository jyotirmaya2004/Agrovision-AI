import json
from functools import lru_cache
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DISEASE_INFO_PATH = BASE_DIR / "disease_info.json"


class DiseaseInfoError(Exception):
    """Raised when disease metadata cannot be loaded."""


@lru_cache(maxsize=1)
def load_disease_info():
    try:
        with DISEASE_INFO_PATH.open("r", encoding="utf-8") as file:
            data = json.load(file)
        return data
    except Exception as e:
        raise DiseaseInfoError(
            f"Unable to load disease info: {e}"
        ) from e


def get_disease_details(class_name):
    disease_data = load_disease_info()
    if class_name in disease_data:
        details = disease_data[class_name]
        return {
            "disease_name": details.get("disease_name", class_name),
            "symptoms": details.get("symptoms", "Not available"),
            "causes": details.get("causes", "Not available"),
            "treatment": details.get("treatment", "Not available"),
            "prevention": details.get("prevention", "Not available"),
        }

    return {
        "disease_name": class_name,
        "symptoms": "Not available",
        "causes": "Not available",
        "treatment": "Not available",
        "prevention": "Not available",
    }
