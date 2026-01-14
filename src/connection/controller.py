#!/usr/bin/env python3
"""Clase comun al resto de archivos del modulo"""

import os
from dataclasses import dataclass

import mysql.connector as mysql
from mysql.connector.connection import MySQLConnection
from mysql.connector.cursor import MySQLCursor
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from dotenv import load_dotenv

from .blueprint import Credentials, SqlStructures

@dataclass
class Connection:
    """Conexion a AWS"""

    path:str

    def __post_init__(self):
        """Se ejecuta luego de instanciar la clase"""

        fullpath = os.path.join(self.path, ".env")
        load_dotenv(fullpath)

    def run_all(self) -> SqlStructures:
        """Ejecuta todo el proceso"""

        credentials = self.get_credentials()
        conector = self.set_connection(credentials)
        cursor = self.set_cursor(conector)
        engine = self.set_engine(credentials)
        return SqlStructures(
            connector=conector,
            cursor=cursor,
            engine=engine,
        )

    def get_credentials(self) -> Credentials:
        """Extrae las credenciales del .env"""

        return Credentials(
            host=os.getenv("HOST"), # type:ignore
            port=os.getenv("PORT"), # type:ignore
            database=os.getenv("DATABASE"), # type:ignore
            user=os.getenv("USER1"), # type:ignore
            password=os.getenv("PSW1"), # type:ignore
        )

    def set_connection(self, credentials:Credentials) -> MySQLConnection:
        """Conexion a la bbdd"""

        try:
            conn = mysql.connect( #type:ignore
                host = credentials.host,
                port = credentials.port,
                database = credentials.database,
                user = credentials.user,
                password = credentials.password,
            )
            print(" -. Conexion a base de datos exitosa...")
            return conn # type:ignore
        except mysql.Error as exc:
            msg = " -- [ERROR]: No se pudo establacer conexion con la base de datos. Verifique."
            raise ConnectionError(msg) from exc

    def set_cursor(self, connector:MySQLConnection) -> MySQLCursor:
        """Genero el cursor de la conexion"""

        return connector.cursor()

    def set_engine(self, credentials:Credentials) -> Engine:
        """Genera el motor"""

        engine = create_engine(
            f"mysql+mysqlconnector://"
            f"{credentials.user}:{credentials.password}@"
            f"{credentials.host}:"
            f"{credentials.port}/"
            f"{credentials.database}"
        )

        return engine
