#!/usr/bin/env python3
"""Orquestador principal del proyecto"""

import os
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path

class Rutas(StrEnum):
    """URLs del proyecto"""

    ROOT_PATH = os.path.abspath(Path(__file__).resolve().parent)
    INE_URL = "https://www.gub.uy/instituto-nacional-estadistica/comunicacion/publicaciones"


class TableNames(StrEnum):
    """Nombres de las tablas"""

    IPC = "t_ipc"
    IMS = "t_ims"
    ICCV = "t_iccv"
