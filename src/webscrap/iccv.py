#!/usr/bin/env python3
"""Descarga, limpia y filtra los datos de ICCV"""

import re
from dataclasses import dataclass, field
from io import StringIO

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .utils import Utils

@dataclass
class IndiceCostoConstruccionVivienda:
    """Obtengo los datos de Nasdaq del ultimo mes"""

    url: str
    month: str
    year: int
    driver: webdriver.Chrome
    xpath:str = '//*[@id="block-starterkits-content"]/article/div/ul/li/a'
    utils: Utils = field(default_factory=Utils)

    def __post_init__(self):
        """Se ejecuta luego de instanciar la clase"""

        print("  -. Obteniendo datos de Indice Costo Construccion de Vivienda...")
        self.url = f"{self.url}/indice-costo-construccion-vivienda-iccv-{self.month}-{self.year}"
        self.utils.check_url_exists(self.url)

    def run_all(self) -> pd.DataFrame:
        """Ejecuta la descarga paso a paso"""

        self.navigate()
        data = self.get_data()
        data = self.clean_data(data)
        return data[[data.columns[-1]] + list(data.columns[:-1])]
        return data

    def navigate(self, wait_time:int=1) -> None:
        """Carga le dataframe desde la web"""

        self.driver.get(self.url)
        elemento = WebDriverWait(self.driver, wait_time).until(
                EC.element_to_be_clickable((By.XPATH, self.xpath))
            )
        elemento.click()

    def get_data(
        self,
        wait_time:int=1,
        table_xpath:str='//*[@id="iccv-por-rubros"]/table',
    ) -> pd.DataFrame:
        """Obtiene la data desde la web"""

        WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located((By.XPATH, table_xpath))
            )

        table = self.driver.find_element(By.XPATH, table_xpath)
        tabla_html = table.get_attribute('outerHTML')
        html_limpio = self.clean_html(tabla_html) # type:ignore
        html_content = StringIO(html_limpio)
        tablas = pd.read_html(html_content, decimal=".", thousands=".")

        if tablas:
            return tablas[0]
        else:
            raise ValueError("  -- [ERROR]: No se encontró la tabla con el ID especificado.")

    def clean_html(self, html:str) -> str:
        """Limpia el html"""

        new_html = html.replace('colspan="100%"', 'colspan="5"') #type:ignore
        new_html = re.sub(r'<tfoot>.*?</tfoot>', '', new_html, flags=re.DOTALL)
        return new_html

    def clean_data(self, data:pd.DataFrame) -> pd.DataFrame:
        """Limpieza de datos"""

        data = data.copy()
        data["Periodo"] = f"{self.month.title()}{self.year}"
        data = data.drop(columns=["Descripción"])
        data.columns = self.set_colnames()
        return data

    def set_colnames(self) -> list[str]:
        """Ajusto nombre de las columnas"""

        return [
            'Rubro',
            'Indice',
            'VariacionMensual',
            'Incidencias',
            'Periodo',
        ]
