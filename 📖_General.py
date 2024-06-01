import streamlit as st

from utils import *


def intro(guide):
    st.markdown("# México: Tendencias de Indicadores Internacionales")
    st.markdown(
        "#### Datos del Banco Mundial para México y otros países comparativos durante los últimos 3 periodos presidenciales."
    )
    cols = st.columns([1, 1])
    with cols[0]:
        st.markdown("")
        st.markdown("")
        st.markdown(
            """
            __En esta sección se presentan las tendencias de algunos de los indicadores internacionales más relevantes, como:__

            - El crecimiento del PIB anual (también per cápita)
            - La tasa de inflación
            - Medidas de desigualdad económica (Índice de Gini) y de pobreza
            - Control de la corrupción
            - Desempleo
            - Gasto público en salud, educación, investigación y desarrollo
            - Adolecencia fuera de la escuela
            - Esperanza de vida.

            En el panel de la izquierda se muestran otras tendencias de indicadores más específicos en cuestiones económicas y sociales. 
            Instrucciones de uso se encuentran en el acordeón de abajo.
            """
        )
    with cols[1]:
        st.markdown("")
        st.markdown("")
        with st.expander(
            "¿Por qué es importante analizar las tendencias de los indicadores internacionales?"
        ):
            st.markdown(
                """       
                    __Analizar las tendencias de los indicadores internacionales de un país es crucial por varias razones:__

                    1. Permite a los ciudadanos y analistas evaluar el desempeño del gobierno actual en áreas clave como economía, salud, educación y gobernanza.
                    2.  Proporciona una base objetiva para comparar las promesas de campaña con los resultados reales logrados durante el mandato.
                    3. Los votantes pueden tomar decisiones más informadas al tener una comprensión clara de la situación actual del país y cómo ha evolucionado en los últimos años.
                    4. Los datos permiten evaluar si las políticas implementadas han sido efectivas o si se necesitan cambios.
                    5. Ayuda a identificar áreas donde ha habido progreso y áreas que requieren más atención.
                    6.  Permite comparar el desempeño del país con el de otras naciones, lo que puede ser útil para identificar mejores prácticas y áreas de mejora.
                 """
            )
    instructions()
    with st.expander("Guía de los indicadores"):
        st.table(guide)


if __name__ == "__main__":

    st.set_page_config(
        page_title="Tendencias (México)",
        page_icon="📊🇲🇽",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.sidebar.title("Menú")
    st.sidebar.image("mex.png")

    data = load_data("./data/General.csv")
    guide = gen_guide()
    intro(guide)
    data = filter_indicator(data)
    data = filter_countries(data)
    expander_country_codes()
    figure_panel(data, guide)
    footer(data)
