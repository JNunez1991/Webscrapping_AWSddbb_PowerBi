#!/usr/bin/env python3
"""
Codigo de ejemplo que se corre dentro de PowerBi
PowerBi no ejecuta este codigo. Solo sirve para ver como correr el script dentro de PowerBi
"""

import sys

from dataclasses import dataclass, field

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

ROOT_DIR = r"C:\Users\javie\Documents\Repositorios\Publicos\AWS_Database"
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from config import Rutas
from src.connection import SetConnection, Credentials


@dataclass
class PowerBi:
    """Obtiene la data desde AWS y la muestra en PowerBi"""

    engine:Engine = field(init=False)

    def __post_init__(self):
        """Se ejecuta luego de instanciar la clase"""

        connection = SetConnection(Rutas.ROOT_PATH)
        credentials = connection.get_credentials()
        self.engine = self.set_engine(credentials)

    def set_engine(self, creds:Credentials) -> Engine:
        """Establece el Engine para extraer la data"""

        string = "mysql+pymysql://"
        string += f"{creds.user}:{creds.password}@"
        string += f"{creds.host}:{creds.port}/{creds.database}"
        return create_engine(string, pool_pre_ping=True)

    def get(self, qry:str) -> pd.DataFrame:
        """Ejecuta cada etapa del proceso"""

        return pd.read_sql(text(qry), self.engine)


powerbi = PowerBi()
QUERY = "CALL sp_get_ipc()"
data = powerbi.get(QUERY)
