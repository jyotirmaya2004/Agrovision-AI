"""Two-stage prediction pipeline.

Stage 1: validate leaf-vs-non-leaf.
Stage 2: if leaf, run disease classification.

This module defines a stable output contract used by the Streamlit UI.
"""

from __future__ import annotations

import json
from functools import lru_cache
from html import escape
from io import BytesIO
from pathlib import Path
from typing import Any, BinaryIO

import numpy as np
import tensorflow as tf
from PIL import Image, UnidentifiedImageError

try:
    from pillow_heif import register_heif_opener
except ImportError:
    register_heif_opener = None

from backend.model_loader import ModelLoadError, load_disease_model, load_leaf_model


BASE_DIR = Path(__file__).resolve().parent.parent
CLASS_NAMES_PATH = BASE_DIR / "model" / "class_names.json"
IMAGE_SIZE = (224, 224)

# This matches current UI threshold semantics.
LEAF_CONFIDENCE_THRESHOLD = 0.5
LEAF_REVIEW_THRESHOLD = 0.35
DISEASE_CONFIDENCE_OVERRIDE = 85.0

if register_heif_opener is not None:
    register_heif_opener()


class PredictionError(Exception):
    """Raised when an image cannot be processed or predicted safely."""


def _load_class_names() -> list[str]:
    try:
        with CLASS_NAMES_PATH.open("r", encoding="utf-8") as f:
            raw = json.load(f)
    except Exception as e:
        raise PredictionError(f"Unable to load class names: {e}") from e

    if isinstance(raw, dict):
        return [raw[k] for k in sorted(raw.keys(), key=lambda x: int(x))]
    if isinstance(raw, list):
        return raw

    raise PredictionError("class_names.json must be a list or dict")


@lru_cache(maxsize=1)
def load_class_names() -> list[str]:
    return _load_class_names()


def format_disease_name(name: str) -> str:
    return name.replace("___", " - ").replace("_", " ").strip()


def _open_image(image_source: str | Path | bytes | BinaryIO | Image.Image) -> Image.Image:
    try:
        if isinstance(image_source, Image.Image):
            image = image_source.copy()
        elif isinstance(image_source, bytes):
            image = Image.open(BytesIO(image_source))
        else:
            if hasattr(image_source, "seek"):
                image_source.seek(0)
            image = Image.open(image_source)
        if getattr(image, "is_animated", False):
            image.seek(0)
        image.load()
    except (UnidentifiedImageError, OSError, ValueError) as e:
        raise PredictionError("Please upload a valid image file.") from e

    return image.convert("RGB")


def _preprocess_for_leaf_validation(image_source: str | Path | bytes | BinaryIO | Image.Image) -> np.ndarray:
    image = _open_image(image_source)
    image = image.resize(IMAGE_SIZE)
    arr = tf.keras.utils.img_to_array(image) / 255.0
    return np.expand_dims(arr, axis=0)


def _normalize_probabilities(raw_predictions: np.ndarray) -> np.ndarray:
    predictions = np.asarray(raw_predictions, dtype=np.float64).reshape(-1)
    if predictions.size == 0 or not np.all(np.isfinite(predictions)):
        raise PredictionError("Disease model returned invalid prediction values.")

    total = float(np.sum(predictions))
    if np.min(predictions) >= 0 and 0.98 <= total <= 1.02:
        return predictions / total

    shifted = predictions - np.max(predictions)
    exp_values = np.exp(shifted)
    exp_total = float(np.sum(exp_values))
    if exp_total <= 0 or not np.isfinite(exp_total):
        raise PredictionError("Disease model probabilities could not be normalized.")

    return exp_values / exp_total


def _predict_disease(base_image: Image.Image, top_k: int) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    try:
        disease_model = load_disease_model()
    except ModelLoadError as e:
        raise PredictionError(str(e)) from e

    class_names = load_class_names()

    # The saved disease model already contains MobileNetV2 preprocessing.
    # Feed raw 0-255 RGB pixels to match the notebook training pipeline.
    disease_img = base_image.resize(IMAGE_SIZE)
    disease_arr = tf.keras.utils.img_to_array(disease_img)
    disease_input = np.expand_dims(disease_arr, axis=0)

    try:
        raw_probabilities = np.asarray(disease_model.predict(disease_input, verbose=0)[0])
    except Exception as e:
        raise PredictionError("The disease model could not make a prediction for this image.") from e

    probabilities = _normalize_probabilities(raw_probabilities)

    if len(probabilities) != len(class_names):
        raise PredictionError(
            "Model output size does not match class_names.json. "
            "Please verify model artifacts."
        )

    top_k = max(1, min(top_k, len(class_names)))
    top_indices = np.argsort(probabilities)[::-1][:top_k]

    top_predictions = [
        {
            "class_name": class_names[idx],
            "disease": format_disease_name(class_names[idx]),
            "confidence": round(float(probabilities[idx]) * 100, 2),
        }
        for idx in top_indices
    ]

    return top_predictions, top_predictions[0]


def predict_two_stage(image_source: str | Path | bytes | BinaryIO | Image.Image, top_k: int = 3) -> dict[str, Any]:
    """Main entrypoint used by UI.

    Returns:
      {
        leaf_validation: {is_leaf, leaf_confidence, non_leaf_confidence, threshold, raw_output_optional}
        disease: str,
        class_name: str,
        confidence: float,
        top_predictions: [{class_name, disease, confidence}, ...]
      }
    """

    try:
        leaf_model = load_leaf_model()
    except ModelLoadError as e:
        raise PredictionError(str(e)) from e

    base_image = _open_image(image_source)
    leaf_input = _preprocess_for_leaf_validation(base_image)

    try:
        raw = np.asarray(leaf_model.predict(leaf_input, verbose=0)[0])
    except Exception as e:
        raise PredictionError("Leaf validation model could not analyze this image.") from e

    raw_flat = raw.reshape(-1)

    # Handle common output formats:
    # - Dense(1, sigmoid): shape (1,) => probability of non_leaf (based on repo comment/notebook)
    # - Dense(2, softmax): shape (2,) => [leaf, non_leaf] or similar.
    if raw_flat.size == 1:
        non_leaf_probability = float(raw_flat[0])
        leaf_probability = 1.0 - non_leaf_probability

        raw_output = {
            "leaf_probability": leaf_probability,
            "non_leaf_probability": non_leaf_probability,
            "non_leaf_probability_raw": non_leaf_probability,
        }
    elif raw_flat.size == 2:
        # Assume [leaf, non_leaf]
        leaf_probability = float(raw_flat[0])
        non_leaf_probability = float(raw_flat[1])
        raw_output = {
            "leaf_probability": leaf_probability,
            "non_leaf_probability": non_leaf_probability,
            "raw_vector": raw_flat.tolist(),
        }
    else:
        raise PredictionError("Leaf validation model output is incompatible with expected binary output.")

    is_leaf = leaf_probability >= LEAF_CONFIDENCE_THRESHOLD

    leaf_validation = {
        "is_leaf": is_leaf,
        "leaf_confidence": round(leaf_probability * 100, 2),
        "non_leaf_confidence": round(non_leaf_probability * 100, 2),
        "threshold": round(LEAF_CONFIDENCE_THRESHOLD * 100, 2),
        "_debug_raw": raw_output,
    }

    if leaf_probability < LEAF_REVIEW_THRESHOLD:
        raise PredictionError(
            "This image does not look like a plant leaf. "
            f"Leaf confidence: {leaf_validation['leaf_confidence']:.2f}%"
        )

    top_predictions, best = _predict_disease(base_image, top_k)
    validation_warning = None
    if not is_leaf and best["confidence"] < DISEASE_CONFIDENCE_OVERRIDE:
        raise PredictionError(
            "This image has low leaf confidence and the disease model is not confident enough. "
            "Please upload a clearer leaf photo."
        )

    if not is_leaf:
        validation_warning = (
            "Leaf validation was borderline, but disease classification was highly confident. "
            "Retake the photo if the result looks wrong."
        )

    # Ensure UI never receives HTML snippets in prediction fields.
    disease_name = escape("" if best["disease"] is None else str(best["disease"]))
    top_predictions = [
        {**tp, "disease": escape("" if tp["disease"] is None else str(tp["disease"]))}
        for tp in top_predictions
    ]

    return {
        "leaf_validation": leaf_validation,
        "class_name": best["class_name"],
        "disease": disease_name,
        "confidence": best["confidence"],
        "top_predictions": top_predictions,
        "validation_warning": validation_warning,
    }
