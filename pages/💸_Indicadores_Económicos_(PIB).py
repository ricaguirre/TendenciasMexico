import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from utils import *


def intro(guide):
    st.markdown("# Tendencias de Indicadores Relacionados al PIB")
    st.markdown("### Resumen")
    st.markdown(
        """
        En ésta sección se presentan las tendencias de los indicadores relacionados 
        con el Producto Interno Bruto (PIB) de México (y otros países comparativos), 
        durante los últimos tres sexenios presidenciales.
        
        Analizar éstas tendencias relacionadas con el PIB proporciona una visión 
        comprensiva y detallada del rendimiento económico y social del país, ayudando 
        a tomar decisiones informadas, ajustar políticas y promover el desarrollo sostenible 
        y equitativo.
    """
    )
    instructions()
    with st.expander("Guía de los indicadores"):
        st.table(guide)


data = load_data("./data/PIB.csv")
guide = pib_guide()
intro(guide)
data = filter_indicator(data)
data = filter_countries(data)
expander_country_codes()
figure_panel(data, guide)

footer(data)
