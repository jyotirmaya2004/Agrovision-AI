from functools import lru_cache
from pathlib import Path

import tensorflow as tf


BASE_DIR = Path(__file__).resolve().parent.parent

DISEASE_MODEL_PATH = BASE_DIR / "model" / "leaf_disease_model.keras"
LEAF_MODEL_PATH = BASE_DIR / "model" / "leaf_vs_non_leaf_model.keras"


class ModelLoadError(Exception):
    """Raised when a model artifact is missing or cannot be loaded."""


@lru_cache(maxsize=1)
def load_disease_model():
    if not DISEASE_MODEL_PATH.exists():
        raise ModelLoadError(
            f"Disease model not found:\n{DISEASE_MODEL_PATH}"
        )

    try:
        return tf.keras.models.load_model(
            DISEASE_MODEL_PATH,
            compile=False,
        )
    except Exception as e:
        raise ModelLoadError(
            f"Unable to load disease model:\n{e}"
        ) from e


@lru_cache(maxsize=1)
def load_leaf_model():
    if not LEAF_MODEL_PATH.exists():
        raise ModelLoadError(
            f"Leaf validation model not found:\n{LEAF_MODEL_PATH}"
        )

    try:
        return tf.keras.models.load_model(
            LEAF_MODEL_PATH,
            compile=False,
        )
    except Exception as e:
        raise ModelLoadError(
            f"Unable to load leaf model:\n{e}"
        ) from e
