import os
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from babel.support import Translations
from typing import Optional

LOCALE_DIR = os.path.join(os.path.dirname(__file__), "../../locales")

class I18nMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        lang = self._detect_language(request)
        request.state.lang = lang
        request.state.translations = self._load_translations(lang)
        response = await call_next(request)
        response.headers["Content-Language"] = lang
        return response

    def _detect_language(self, request: Request) -> str:
        # Check Accept-Language header or query param
        lang = request.query_params.get("lang")
        if lang:
            return lang
        accept_lang = request.headers.get("accept-language")
        if accept_lang:
            return accept_lang.split(",")[0]
        return "en"

    def _load_translations(self, lang: str) -> Optional[Translations]:
        try:
            return Translations.load(LOCALE_DIR, [lang])
        except Exception:
            return None
