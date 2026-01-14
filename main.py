#!/usr/bin/env python3
"""Orquestador principal del proyecto"""

from dataclasses import dataclass, field, asdict

from config import Rutas, Meses, TableNames
from src.utils import Utils
from src.webscrap import Webscrapping
from src.connection import SetConnection


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
        conection = SetConnection(Rutas.ROOT_PATH)
        conn = conection.run_all()

        # Llamo al controller que orquesta la descarga de informacion
        webscr = Webscrapping(Rutas.INE_URL, mes, anio)
        data = webscr.run_all()

        # Guardo la data en bbdd
        conection.to_datablase(data.ipc, TableNames.IPC, conn.engine)
        conection.to_datablase(data.ims, TableNames.IMS, conn.engine)
        conection.to_datablase(data.iccv, TableNames.ICCV, conn.engine)

        return data


if __name__ == "__main__":

    main = Main()
    dataframes = main.run_all()
