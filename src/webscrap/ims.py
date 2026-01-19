#!/usr/bin/env python3
"""Descarga, limpia y filtra los datos de IMS"""

import re
from dataclasses import dataclass, field
from datetime import date
from io import StringIO

import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .utils import Utils

@dataclass
class IndiceMedioSalarios:
    """Obtengo los datos de Nasdaq del ultimo mes"""

    url: str
    period: date
    str_month: str
    driver: webdriver.Chrome
    year: int = field(init=False)
    xpath:str = '//*[@id="block-starterkits-content"]/article/div/ul/li/a'
    utils: Utils = field(default_factory=Utils)

    def __post_init__(self):
        """Se ejecuta luego de instanciar la clase"""

        print("  -. Obteniendo datos de Indice Medio de Salarios...")
        self.year = self.period.year
        self.url = f"{self.url}/indice-medio-salarios-ims-{self.str_month}-{self.year}"
        self.utils.check_url_exists(self.url)

    def run_all(self) -> pd.DataFrame:
        """Ejecuta la descarga paso a paso"""

        self.navigate()
        data = self.get_data()
        data = self.clean_data(data)
        return data

    def navigate(self, wait_time:int=1) -> None:
        """Carga le dataframe desde la web"""

        self.driver.get(self.url)
        elemento = WebDriverWait(self.driver, wait_time).until(
                EC.element_to_be_clickable((By.XPATH, self.xpath))
            )
        elemento.click()

    def get_data(self, wait_time:int=1) -> pd.DataFrame:
        """Obtiene la data desde la web"""

        table_xpath=f'//*[@id="{self.str_month}-{self.year-1}---{self.str_month}-{self.year}"]/div[2]/table'
        WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located((By.XPATH, table_xpath))
            )

        table = self.driver.find_element(By.XPATH, table_xpath)
        tabla_html = table.get_attribute('outerHTML')
        html_limpio = self.clean_html(tabla_html) # type:ignore
        html_content = StringIO(html_limpio)
        html_content = StringIO(tabla_html)
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
        data = self.adjust_data(data)
        data = self.filter_data(data)
        data["periodo"] = self.period
        data = data[[data.columns[-1]] + list(data.columns[:-1])]
        data.columns = self.set_colnames()
        return data

    def adjust_data(self, data:pd.DataFrame) -> pd.DataFrame:
        """Ajusto valores faltantes y transformo columnas a float"""

        data = data.dropna(ignore_index=True)
        data = data.replace(r"\(\s*s\s*\)", np.nan, regex=True)
        data.iloc[:,1:] = data.iloc[:,1:].replace(",", ".", regex=True).astype(float)
        data.iloc[:,0] = data.iloc[:,0].str[0] # me quedo con la primer letra
        return data

    def filter_data(self, data:pd.DataFrame) -> pd.DataFrame:
        """Para proyecto de ejemplo, me quedo solo con las categorias"""

        col = data.columns[0]
        data = data[data[col].str.match(r"^[A-Za-z]")]
        data = data.iloc[1:,:].reset_index(drop=True)
        return data

    def set_colnames(self) -> list[str]:
        """Ajusto nombre de las columnas"""

        return [
            'periodo',
            'id_sector',
            'indice',
            'mes',
            'acum_anual',
            'ultimos_doce_meses',
            'incidencias',
        ]
