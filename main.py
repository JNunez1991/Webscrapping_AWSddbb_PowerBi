#!/usr/bin/env python3
"""Orquestador principal del proyecto"""

from dataclasses import dataclass, field

from config import Rutas, TableNames
from src.connection import SetConnection
from src.utils import Utils
from src.webscrap import Webscrapping


@dataclass
class Main:
    """Clase principal que se encarga de orquestar el webscrapping y la persistencia de datos"""

    utils:Utils = field(default_factory=Utils)

    def run_all(self) -> None:
        """Ejecuta el proceso paso a paso"""

        # Titulo en consola
        self.utils.print_header("Webscrapping & AWS storage")

        # Obtiene año/mes desde el usuario
        anio, mes = self.utils.user_input()
        str_mes = self.utils.month_to_string(mes)
        full_date = self.utils.period_date(anio, mes)

        # Conexion a la bbdd de AWS (connection, cursor & engine)
        conection = SetConnection(Rutas.ROOT_PATH)
        engine = conection.get_engine()

        # Llamo al controller que orquesta la descarga de informacion
        webscr = Webscrapping(Rutas.INE_URL, full_date, str_mes)
        data = webscr.run_all()

        # Guardo la data en bbdd
        conection.to_database(data.ipc, TableNames.IPC, engine)
        conection.to_database(data.ims, TableNames.IMS, engine)
        conection.to_database(data.iccv, TableNames.ICCV, engine)


if __name__ == "__main__":

    main = Main()
    main.run_all()
