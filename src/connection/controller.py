#!/usr/bin/env python3
"""Clase comun al resto de archivos del modulo"""

import os
from dataclasses import dataclass
from typing import Iterable

import pandas as pd
import mysql.connector as mysql
from dotenv import load_dotenv
from mysql.connector.connection import MySQLConnection
from mysql.connector.cursor import MySQLCursor
from pandas.io.sql import SQLTable
from sqlalchemy import create_engine, text
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.engine import Engine
from sqlalchemy.engine import Connection

from .blueprint import Credentials, SqlStructures

@dataclass
class SetConnection:
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
            print("  -. Conexion exitosa a base de datos...")
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

    def to_datablase(
        self,
        data:pd.DataFrame,
        tablename:str,
        engine:Engine,
    ) -> None:
        """Almacena la data en bbdd, y cuenta los registros persistidos"""

        before = self.get_total_rows(tablename, engine)
        self.data_to_ddbb(data, tablename, engine)
        after = self.get_total_rows(tablename, engine)
        print(f"    --> Se añadieron {after - before} registros en la tabla '{tablename}'")


    def get_total_rows(
        self,
        tablename:str,
        engine:Engine,
        stored_procedure:str = "sp_total_rows"
    ) -> int:
        """Cuenta la cantidad de filas en cierta tabla"""

        with engine.begin() as conn:
            conn.execute(
                text(f"CALL {stored_procedure}(:table, @total)"),
                {"table": tablename}
            )
            return conn.execute(text("SELECT @total")).scalar() # type:ignore

    def data_to_ddbb(
        self,
        data:pd.DataFrame,
        tablename:str,
        engine:Engine,
    ) -> None:
        """Persiste la data en bbdd"""

        try:
            data.to_sql(
                name=tablename,
                con=engine,
                if_exists="append",
                index=False,
                method=self.insert_ignore,
            )
        except mysql.Error as exc:
            msg = f"    --> [ERROR]: No se pudieron persistir los datos en '{tablename}'"
            raise ConnectionError(msg) from exc

    def insert_ignore(
        self,
        table:SQLTable,
        conn:Connection,
        keys:list[str],
        data_iter:Iterable[tuple],
    ) -> None:
        """
        Persiste datos en bbdd ignorando duplicados.
        Es decir, si el dato ya existe, no lo vuelve a guardar.
        """
        data = [dict(zip(keys, row)) for row in data_iter]
        stmt = insert(table.table).values(data)
        stmt = stmt.prefix_with("IGNORE")
        conn.execute(stmt)
