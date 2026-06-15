import json
from functools import lru_cache
from pathlib import Path

import streamlit as st


BASE_DIR = Path(__file__).resolve().parent.parent
DISEASE_INFO_PATH = BASE_DIR / "disease_info.json"
UI_TRANSLATIONS_PATH = BASE_DIR / "ui_translations.json"


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


@lru_cache(maxsize=1)
def load_static_translations():
    try:
        if UI_TRANSLATIONS_PATH.exists():
            with UI_TRANSLATIONS_PATH.open("r", encoding="utf-8") as file:
                return json.load(file)
    except Exception as e:
        print(f"Failed to load static UI translations: {e}")
    return {}

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


@st.cache_data(show_spinner=False, ttl=3600)
def translate_disease_info(info_dict: dict, target_lang_code: str) -> dict:
    if target_lang_code == 'en':
        return info_dict

    try:
        static_trans = load_static_translations()
        translated_info = {}
        for key, value in info_dict.items():
            if value and value != "Not available":
                if target_lang_code in static_trans and value in static_trans[target_lang_code]:
                    translated_info[key] = static_trans[target_lang_code][value]
                else:
                    translated_info[key] = value
            else:
                translated_info[key] = value
        return translated_info
    except Exception as e:
        print(f"Disease Info Translation failed: {e}")
        return info_dict

def translate_text(text: str, target_lang_code: str) -> str:
    if target_lang_code == 'en' or not text:
        return text

    static_trans = load_static_translations()
    if target_lang_code in static_trans and text in static_trans[target_lang_code]:
        return static_trans[target_lang_code][text]

    return text

def _t(text: str) -> str:
    lang_code = st.session_state.get("lang_code", "en")
    if lang_code == "en" or not text:
        return text
    return translate_text(text, lang_code)
