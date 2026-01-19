#!/usr/bin/env python3
"""Orquestador principal de webscrapping"""

from dataclasses import dataclass
from datetime import date

from selenium import webdriver

from .blueprint import StoredOutputs
from .ipc import IndicePreciosConsumo
from .ims import IndiceMedioSalarios
from .iccv import IndiceCostoConstruccionVivienda


@dataclass
class Webscrapping:
    """Obtengo los datos de Nasdaq del ultimo mes"""

    url: str
    period: date
    str_month: str

    def run_all(self) -> StoredOutputs:
        """Ejecuta la descarga paso a paso"""

        driver = self.set_driver()

        # Datos de IPC
        ipc = IndicePreciosConsumo(self.url, self.period, self.str_month, driver)
        data_ipc = ipc.run_all()

        # Datos de IMS
        ims = IndiceMedioSalarios(self.url, self.period, self.str_month, driver)
        data_ims = ims.run_all()

        # Datos de ICCV
        iccv = IndiceCostoConstruccionVivienda(self.url, self.period, self.str_month, driver)
        data_iccv = iccv.run_all()

        # Cierro driver
        driver.quit()

        return StoredOutputs(
            ipc=data_ipc,
            ims=data_ims,
            iccv=data_iccv,
        )


    def set_driver(self) -> webdriver.Chrome:
        """Setea el navegador web"""

        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        drv = webdriver.Chrome(options=options)
        return drv
