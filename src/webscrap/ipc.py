#!/usr/bin/env python3
"""Descarga, limpia y filtra los datos de IPC"""

from dataclasses import dataclass, field
from datetime import date
from io import StringIO

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .utils import Utils

@dataclass
class IndicePreciosConsumo:
    """Obtengo los datos de Inflacion del ultimo mes"""

    url: str
    period: date
    str_month: str
    driver: webdriver.Chrome
    year:int = field(init=False)
    xpath:str = '//*[@id="block-starterkits-content"]/article/div/ul/li/a'
    utils: Utils = field(default_factory=Utils)

    def __post_init__(self):
        """Se ejecuta luego de instanciar la clase"""

        print("  -. Obteniendo datos de Indice de Precios al Consumo...")
        self.year = self.period.year
        self.url = f"{self.url}/indice-precios-del-consumo-ipc-{self.str_month}-{self.year}"
        self.utils.check_url_exists(self.url)

    def run_all(self) -> pd.DataFrame:
        """Ejecuta la descarga paso a paso"""

        self.navigate()
        data = self.get_data()
        data = self.clean_data(data)
        data.columns = self.set_colnames()
        data.id_division = data.id_division.astype(int)
        return data

    def navigate(
        self,
        wait_time:int=1,
    ) -> None:
        """Carga le dataframe desde la web"""

        self.driver.get(self.url)
        elemento = WebDriverWait(self.driver, wait_time).until(
                EC.element_to_be_clickable((By.XPATH, self.xpath))
            )
        elemento.click()

    def get_data(
        self,
        wait_time:int=3,
        table_id:str = "DataTables_Table_0",
    ) -> pd.DataFrame:
        """Obtiene la data desde la web"""

        WebDriverWait(self.driver, wait_time).until(
            EC.presence_of_element_located((By.ID, table_id))
        )
        html_content = StringIO(self.driver.page_source)
        tablas = pd.read_html(html_content, attrs={'id': table_id})
        if tablas:
            return tablas[0]
        else:
            raise ValueError("  -- [ERROR]: No se encontró la tabla con el ID especificado.")

    def clean_data(
        self,
        data:pd.DataFrame,
        keep="TOTAL PAIS",
    ) -> pd.DataFrame:
        """Limpieza de datos"""

        data = data.copy()
        data = data.dropna(ignore_index=True)
        data = data[data["Nombre"] == keep]
        data = data.drop(data.columns[2], axis=1) # borro la columna de 'Descripcion'
        data.iloc[:,0] = self.period
        return data

    def set_colnames(self) -> list[str]:
        """Nombres de columnas"""

        return [
            'periodo',
            'id_division',
            'ponderacion',
            'indice',
            'var_mensual',
            'var_ac_anual',
            'var_doce_meses',
            'incidencia',
        ]
