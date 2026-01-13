#!/usr/bin/env python3
"""Orquestador principal de webscrapping"""

from dataclasses import dataclass

import pandas as pd

@dataclass
class StoredOutputs:
    """Clase donde se almacena la data scrappeada"""

    ipc: pd.DataFrame
    ims: pd.DataFrame
    iccv: pd.DataFrame
