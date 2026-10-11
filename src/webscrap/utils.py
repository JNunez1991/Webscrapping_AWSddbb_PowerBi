#!/usr/bin/env python3
"""Funciones auxiliares"""

from dataclasses import dataclass

import requests


@dataclass
class Utils:
    """Clases auxiliares"""

    def check_url_exists(self, url:str) -> bool:
        """Chequea si una pagina web existe o no"""

        respuesta = requests.head(url, timeout=10, allow_redirects=True)
        if respuesta.status_code < 400:
            return True
        raise ValueError(f"  -- [ERROR]: La pagina solicitada '{url}' no existe. Verifique.")
