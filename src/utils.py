#!/usr/bin/env python3
"""Funciones auxiliares"""

from dataclasses import dataclass, asdict
from datetime import date

import arrow
import pyfiglet

@dataclass(frozen=True)
class Meses:
    """Meses del año"""

    enero: int = 1
    febrero: int = 2
    marzo: int = 3
    abril: int = 4
    mayo: int = 5
    junio: int = 6
    julio: int = 7
    agosto: int = 8
    septiembre: int = 9
    octubre: int = 10
    noviembre: int = 11
    diciembre: int = 12

@dataclass
class Utils:
    """Funciones auxiliares"""

    def print_header(self, texto:str, font="slant") -> None:
        """Titulo en consola"""

        titulo = pyfiglet.figlet_format(texto, font=font)
        print(titulo)

    def user_input(self) -> tuple[int, int]:
        """Mes y Año ingresado por el usuario"""

        while True:
            year = self.user_year()
            month = self.user_month()

            now = arrow.now().date()
            current_year, current_month = now.year, now.month

            if (year, month) <= (current_year, current_month):
                return year, month
            else:
                tope = f"{current_month}/{current_year}"
                msg = f"  -- [ERROR]: La combinación mes/año debe ser menor a {tope} "
                print(msg)

    def user_year(self) -> int:
        """El usuario ingresa el año"""

        while True:
            try:
                anio = int(input("Introduzca un año (2023 o posterior): "))
                if anio >= 2023:
                    return anio
                else:
                    print("  -- [ERROR]: El año debe ser mayor o igual a 2023.")
            except ValueError:
                print("  -- [ERROR]: Por favor, introduce un número entero válido.")

    def user_month(self) -> int:
        """El usuario ingresa el año"""

        while True:
            try:
                mes = int(input("Introduce un número de mes (1-12): "))
                if 1 <= mes <= 12:
                    return mes
                else:
                    print("  -- [ERROR]: El mes debe estar entre 1 y 12.")
            except ValueError:
                print("  -- [ERROR]: Por favor, introduce un número entero válido.")

    def period_date(self, year:int, month:int, day:int=1) -> date:
        """Genera la fecha"""

        return date(year, month, day)

    def month_to_string(self, month:int) -> str:
        """Transforma el numero de mes en su correspondiente nombre"""

        meses = asdict(Meses())
        meses_invertido = { v: k for k, v in meses.items() }
        return meses_invertido[month].lower()
