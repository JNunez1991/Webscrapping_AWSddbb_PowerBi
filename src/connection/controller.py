#!/usr/bin/env python3
"""Clase comun al resto de archivos del modulo"""

import os
from dataclasses import dataclass
from typing import Iterable

import pandas as pd
from dotenv import load_dotenv
from pandas.io.sql import SQLTable
from sqlalchemy import create_engine, text
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.engine import Connection, Engine
from sqlalchemy.exc import SQLAlchemyError

from .blueprint import Credentials

@dataclass
class SetConnection:
    """Conexion a AWS"""

    path:str

    def __post_init__(self):
        """Se ejecuta luego de instanciar la clase"""

        fullpath = os.path.join(self.path, ".env")
        load_dotenv(fullpath)

    def get_engine(self) -> Engine:
        """Ejecuta todo el proceso"""

        credentials = self.get_credentials()
        return self.set_engine(credentials)

    def get_credentials(self) -> Credentials:
        """Extrae las credenciales del .env"""

        return Credentials(
            host=os.getenv("HOST"), # type:ignore
            port=os.getenv("PORT"), # type:ignore
            database=os.getenv("DATABASE"), # type:ignore
            user=os.getenv("USER1"), # type:ignore
            password=os.getenv("PSW1"), # type:ignore
        )

    def set_engine(self, credentials:Credentials) -> Engine:
        """
        Genera el motor, el cual se encarga de:
            - Abrir la conexion
            - La devuelve al pool
            - Hace commit / rollbach
            - Maneja errores
            - Evita dejar conexiones abiertas
        """

        return create_engine(
            f"mysql+pymysql://"
            f"{credentials.user}:{credentials.password}@"
            f"{credentials.host}:"
            f"{credentials.port}/"
            f"{credentials.database}",
            pool_pre_ping=True,
            future=True,
        )

    def to_database(
        self,
        data:pd.DataFrame,
        tablename:str,
        engine:Engine,
    ) -> None:
        """Almacena la data en bbdd, y cuenta los registros persistidos"""

        before = self.get_total_rows(tablename, engine)
        self.data_to_ddbb(data, tablename, engine)
        after = self.get_total_rows(tablename, engine)

        rows = after - before
        if rows > 0:
            print(f"    --> Se añadieron {after - before} registros en la tabla '{tablename}'")
            return
        print(f"    --> No se añadieron nuevos registros en {tablename}")

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
        except SQLAlchemyError as exc:
            msg = f"    --> [ERROR]: No se pudieron persistir los datos en '{tablename}'"
            raise ConnectionError(msg) from exc

    def insert_ignore(
        self,
        table:SQLTable,
        conn:Connection,
        keys:list[str],
        data_iter:Iterable[tuple],
    ) -> int:
        """
        Persiste datos en bbdd ignorando duplicados.
        Es decir, si el dato ya existe, no lo vuelve a guardar.
        """
        data = [dict(zip(keys, row)) for row in data_iter]
        stmt = insert(table.table).values(data).prefix_with("IGNORE")
        result = conn.execute(stmt)
        return result.rowcount
