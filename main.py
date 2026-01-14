#!/usr/bin/env python3
"""Orquestador principal del proyecto"""

from dataclasses import dataclass, field, asdict

from config import Rutas, Meses
from src.utils import Utils
from src.webscrap import Webscrapping
from src.connection import Connection


@dataclass
class Main:
    """Clase principal que se encarga de orquestar el webscrapping y la persistencia de datos"""

    utils:Utils = field(init=False)

    def __post_init__(self):
        """Se ejecuta luego de instanciar la clase"""

        meses = asdict(Meses())
        self.utils = Utils(meses)

    def run_all(self):
        """Ejecuta el proceso paso a paso"""

        # Obtiene año/mes desde el usuario
        anio, mes = self.utils.user_input()
        mes = self.utils.month_to_string(mes)

        # Conexion a la bbdd de AWS (connection, cursor & engine)
        conection = Connection(Rutas.ROOT_PATH)
        conn = conection.run_all()

        # Llamo al controller que orquesta la descarga de informacion
        webscr = Webscrapping(Rutas.INE_URL, mes, anio)
        data = webscr.run_all()


        return conn, data


if __name__ == "__main__":

    main = Main()
    results = main.run_all()
