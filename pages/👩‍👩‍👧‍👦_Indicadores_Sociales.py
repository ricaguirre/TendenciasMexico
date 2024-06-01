import streamlit as st

from utils import *


def intro(guide):
    st.markdown("# Tendencias de Indicadores Sociales")
    st.markdown("### Resumen")
    st.markdown(
        """
        En ésta sección se presentan las tendencias de algunos de los indicadores relevantes en cuestiones sociales, como:

        ###### Educación
        - Adolescentes fuera de la escuela (% de la edad de la escuela secundaria inferior)  _"Adolescents out of school (% of lower secondary school age)"_
        - Tasa de alfabetización, total de adultos (% de personas de 15 años y más) _"Literacy rate, adult total (% of people ages 15 and above)"_
        - Gasto del gobierno en educación, total (% del PIB) _"Government expenditure on education, total (% of GDP)"_

        ###### Pobreza
        - Tasa de pobreza según la línea de pobreza social (% de la población) _"Poverty headcount ratio at national poverty lines (% of population)"_
        - Tasa de pobreza según $$2.15 al día (2017 PPA) (% de la población) _"Poverty headcount ratio at $2.15 a day (2017 PPP) (% of population)"_
        - Tasa de pobreza multidimensional (Banco Mundial) (% de la población) _"Multidimensional poverty headcount ratio (% of population)"_

        ###### Desempleo
        - Desempleo, total (% de la fuerza laboral total) (estimación OIT modelada) _"Unemployment, total (% of total labor force) (modeled ILO estimate)"_

        """
    )
    instructions()
    with st.expander("Guía de los indicadores"):
        st.table(guide)

st.sidebar.title("Menú")
st.sidebar.image("./mex.png")
data = load_data("./data/Social.csv")
# st.dataframe(data["Series Name"].unique())
guide = social_guide()
intro(guide)
data = filter_indicator(data)
data = filter_countries(data)
expander_country_codes()
figure_panel(data, guide)
footer(data)
