import json
import os
from typing import Dict

LOCALES_DIR = os.path.join(os.path.dirname(__file__), "../../locales")

_cache = {}


async def get_translation(guild_id: int, key: str, **kwargs) -> str:
    lang = "en"  # For demo, fixed language; in real app detect per guild/user
    translations = _cache.get(lang)
    if translations is None:
        path = os.path.join(LOCALES_DIR, f"{lang}.json")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                translations = json.load(f)
                _cache[lang] = translations
        else:
            translations = {}
    text = translations.get(key, key)
    if kwargs:
        try:
            text = text.format(**kwargs)
        except Exception:
            pass
    return text
