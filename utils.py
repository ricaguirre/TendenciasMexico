import pandas as pd
import plotly.graph_objects as go
import streamlit as st


@st.cache_data
def load_data(path: str):
    data = pd.read_csv(f"{path}")
    data.columns = data.columns.str.replace(r"\s*\[.*?\]\s*", "", regex=True)
    data = data.drop(columns=["Country Name", "Series Code"])
    data = data.dropna()
    return data


def expander_country_codes():
    with st.expander("Guía de códigos por país"):
        st.markdown(
            """
                    | Código       | País |
                    |:------------:|:-----:|
                    | MEX          | México|
                    | USA          | Estados Unidos|
                    | BRA          | Brasil|
                    | CHL          | Chile|
                    | SLV          | El Salvador|
                    | ESP          | España|
                    | DEU          | Alemania|
                    """
        )


def instructions():
    with st.expander("__Instrucciones de Uso:__"):
        st.markdown(
            """
            1. (Opcional) Despliega el acordeón "Guía de los indicadores" para ver la descripción de los indicadores disponibles.
            2. Selecciona el indicador (con nombre en inglés, la traducción está en la Guía de los indicadores)
            3. Selecciona los países de interés.
            4. Observa la tendencia de los indicadores seleccionados.
            """
        )


def filter_indicator(data):
    indicator = st.selectbox(
        "Escoge el Indicador", list(data["Series Name"].unique()), 4
    )
    data = data[data["Series Name"] == indicator]
    return data


def filter_countries(data):
    countries = st.multiselect(
        "Escoge los países para ver su tendencia",
        list(data["Country Code"].unique()),
        ["MEX"],
    )
    data = data[data["Country Code"].isin(countries)]
    return data


def show_trend(df: pd.DataFrame):
    df = df.drop(columns=["Series Name"])
    df = df.set_index("Country Code")
    countries = list(df.index.unique())
    traces = []
    for country in countries:
        trace = go.Scatter(
            x=list(df.columns),
            y=df.loc[country],
            mode="lines+markers",
            name=country,
            showlegend=True,
        )
        traces.append(trace)
    fig = go.Figure(data=traces)
    fig.update_layout(xaxis=dict(tickmode="array", tickvals=list(df.columns)))
    fig = fig_template(fig)
    st.plotly_chart(fig)


def fig_template(fig: go.Figure):
    fig.add_shape(
        type="rect",
        xref="x",
        yref="paper",
        x0="2005",
        y0=0,
        x1="2006",
        y1=1.1,
        fillcolor="#297eef",
        opacity=0.4,
        layer="below",
        line_width=0,
    )
    fig.add_shape(
        type="rect",
        xref="x",
        yref="paper",
        x0="2006",
        y0=0,
        x1="2012",
        y1=1.2,
        fillcolor="#2672d7",
        opacity=0.3,
        layer="below",
        line_width=0,
        label=dict(
            text="PAN<br>(Calderón)",
            textposition="top center",
            font=dict(color="black", size=16),
        ),
    )
    fig.add_shape(
        type="rect",
        xref="x",
        yref="paper",
        x0="2012",
        y0=0,
        x1="2018",
        y1=1.2,
        fillcolor="#497e49",
        opacity=0.3,
        layer="below",
        line_width=0,
        label=dict(
            text="PRI<br>(Peña Nieto)",
            textposition="top center",
            font=dict(color="black", size=16),
        ),
    )
    fig.add_shape(
        type="rect",
        xref="x",
        yref="paper",
        x0="2018",
        y0=0,
        x1="2023",
        y1=1.2,
        fillcolor="#da2c24",
        opacity=0.3,
        layer="below",
        line_width=0,
        label=dict(
            text="MORENA<br>(AMLO)",
            textposition="top center",
            font=dict(color="black", size=16),
        ),
    )
    return fig


def figure_panel(data, guide):
    st.markdown("")
    st.markdown("")
    if not data.empty:
        cols = st.columns([3, 0.2, 1])
        with cols[2]:
            indicator = data["Series Name"].iloc[0]
            title = guide.loc[indicator, "Traducción"]
            definition = guide.loc[indicator, "Definición"]
            purpose = guide.loc[indicator, "Propósito"]
            importance = guide.loc[indicator, "Importancia"]
            st.markdown("")
            st.markdown("")
            st.markdown("")
            st.markdown("")
            st.markdown(
                f"""
                        #### Definición
                        {definition}

                        #### Propósito
                        {purpose}

                        #### Importancia
                        {importance}
                        """
            )

        with cols[0]:
            st.markdown(f"### {title}")
            show_trend(data)

    else:
        st.warning("Seleccione algún país para ver la tendencia.")


def footer(data):
    st.markdown("---")
    cb = st.checkbox("Mostrar Datos")
    if cb:
        st.write("### Datos")
        st.dataframe(data.set_index("Country Code"))
    st.markdown("---")
    st.markdown(
        "Fuente: [Base de Datos del Banco Mundial](https://data.worldbank.org/)"
    )
    st.markdown("Creado por: Ric Aguirre")


def gen_guide():
    data = {
        "Nombre en inglés": [
            "GDP per capita, PPP (constant 2021 international $)",
            "GDP growth (annual %)",
            "Inflation, GDP deflator (annual %)",
            "Gini index",
            "Control of Corruption: Estimate",
            "Control of Corruption: Percentile Rank",
            "Research and development expenditure (% of GDP)",
            "Domestic general government health expenditure (% of GDP)",
            "Government expenditure on education, total (% of GDP)",
            "Adolescents out of school (% of lower secondary school age)",
            "Literacy rate, adult total (% of people ages 15 and above)",
            "Multidimensional poverty headcount ratio (World Bank) (% of population)",
            "Unemployment, total (% of total labor force) (modeled ILO estimate)",
            "Life expectancy at birth, total (years)",
        ],
        "Traducción": [
            "PIB per cápita, PPA (constante 2021 $ internacional)",
            "Crecimiento del PIB (anual %)",
            "Inflación, deflactor del PIB (anual %)",
            "Índice de Gini",
            "Control de la Corrupción: Estimación",
            "Control de la Corrupción: Rango Percentil",
            "Gasto en investigación y desarrollo (% del PIB)",
            "Gasto interno del gobierno general en salud (% del PIB)",
            "Gasto del gobierno en educación, total (% del PIB)",
            "Adolescentes fuera de la escuela (% de la edad de la escuela secundaria inferior)",
            "Tasa de alfabetización, total de adultos (% de personas de 15 años y más)",
            "Tasa de pobreza multidimensional (Banco Mundial) (% de la población)",
            "Desempleo, total (% de la fuerza laboral total) (estimación OIT modelada)",
            "Esperanza de vida al nacer, total (años)",
        ],
        "Definición": [
            "PIB per cápita ajustado por PPA en dólares internacionales constantes de 2021.",
            "Tasa anual de crecimiento del Producto Interno Bruto.",
            "Tasa anual de inflación medida por el deflactor del PIB.",
            "Medida de la desigualdad en la distribución del ingreso. __Un valor de 0 indica perfecta igualdad (todos tienen el mismo ingreso) y un valor de 100 indica perfecta desigualdad (donde una sola persona tiene todo el ingreso y los demás no tienen nada).__",
            "Estimación del control de la corrupción en un país. Escala de -2.5 a 2.5. __Un número más cercano a 2.5 (positivo) indica un mejor control sobre la corrupción.__",
            "Rango percentil del control de la corrupción en un país. __Un número más cercano a 100 indica un mejor control sobre la corrupción__.",
            "Gasto en investigación y desarrollo como porcentaje del PIB.",
            "Gasto del gobierno general en salud como porcentaje del PIB.",
            "Total del gasto gubernamental en educación en relación al PIB.",
            "Porcentaje de adolescentes de edad de secundaria inferior que no asisten a la escuela.",
            "Porcentaje de adultos de 15 años o más que pueden leer y escribir.",
            "Porcentaje de la población que sufre pobreza multidimensional según el Banco Mundial.",
            "Porcentaje de la fuerza laboral total que está desempleada según estimación modelada de la OIT.",
            "Número promedio de años que se espera que viva una persona desde su nacimiento.",
        ],
        "Propósito": [
            "Medir el nivel de riqueza promedio ajustado por el costo de vida.",
            "Evaluar el crecimiento económico de un país.",
            "Medir el nivel de inflación de una economía.",
            "Medir la desigualdad económica en una sociedad.",
            "Evaluar la percepción del control de la corrupción.",
            "Evaluar la posición relativa del control de la corrupción en un país.",
            "Medir la inversión en innovación y desarrollo.",
            "Evaluar la inversión pública en salud.",
            "Evaluar la inversión pública en educación.",
            "Medir la exclusión educativa entre adolescentes.",
            "Medir el nivel de alfabetización entre adultos.",
            "Medir la proporción de población en pobreza multidimensional.",
            "Medir la tasa de desempleo total según estimaciones internacionales.",
            "Evaluar la salud y el bienestar general de la población.",
        ],
        "Importancia": [
            "Refleja el bienestar económico y el nivel de vida de los ciudadanos.",
            "Indica la expansión económica y el desarrollo del país.",
            "Refleja el poder adquisitivo y estabilidad económica.",
            "Indica la equidad en la distribución de ingresos.",
            "Refleja la eficacia de las políticas anticorrupción.",
            "Refleja la calidad de las instituciones gubernamentales.",
            "Indica el compromiso con la innovación y el crecimiento económico.",
            "Refleja la prioridad del gobierno en la salud pública.",
            "Refleja la prioridad del gobierno en el desarrollo educativo.",
            "Refleja el acceso y permanencia en la educación secundaria.",
            "Refleja el nivel de alfabetización y educación básica de los adultos.",
            "Refleja múltiples dimensiones de la pobreza más allá del ingreso.",
            "Refleja la salud del mercado laboral según estándares internacionales.",
            "Indica el nivel de desarrollo y calidad de vida en el país.",
        ],
    }
    df = pd.DataFrame(data)
    df = df.set_index("Nombre en inglés")
    return df


def pib_guide():
    data = {
        "Nombre en inglés": [
            "Central government debt, total (% of GDP)",
            "Domestic general government health expenditure (% of GDP)",
            "Expense (% of GDP)",
            "Foreign direct investment, net inflows (% of GDP)",
            "GDP per capita growth (annual %)",
            "GDP per capita (current US$)",
            "GDP per capita (current LCU)",
            "GDP growth (annual %)",
            "GDP per capita, PPP (constant 2021 international $)",
            "GDP per capita, PPP (current international $)",
            "GDP per person employed (constant 2021 PPP $)",
            "Government expenditure on education, total (% of GDP)",
            "General government final consumption expenditure (% of GDP)",
            "Inflation, GDP deflator (annual %)",
            "Gross capital formation (% of GDP)",
            "Gross domestic savings (% of GDP)",
            "Gross fixed capital formation (% of GDP)",
            "Gross fixed capital formation, private sector (% of GDP)",
            "Gross national expenditure (% of GDP)",
            "Gross savings (% of GDP)",
            "Military expenditure (% of GDP)",
            "Research and development expenditure (% of GDP)",
        ],
        "Traducción": [
            "Deuda total del gobierno central (% del PIB)",
            "Gasto en salud del gobierno general doméstico (% del PIB)",
            "Gasto (% del PIB)",
            "Inversión extranjera directa, entradas netas (% del PIB)",
            "Crecimiento del PIB per cápita (anual %)",
            "PIB per cápita (US$ actuals)",
            "PIB per cápita (moneda local actual)",
            "Crecimiento del PIB (anual %)",
            "PIB per cápita, PPA (dólares internacionales constantes de 2021)",
            "PIB per cápita, PPA (dólares internacionales actuals)",
            "PIB por persona empleada (PPA constante de 2021)",
            "Gasto del gobierno en educación, total (% del PIB)",
            "Gasto de consumo final del gobierno general (% del PIB)",
            "Inflación, deflactor del PIB (anual %)",
            "Formación bruta de capital (% del PIB)",
            "Ahorro interno bruto (% del PIB)",
            "Formación bruta de capital fijo (% del PIB)",
            "Formación bruta de capital fijo, sector privado (% del PIB)",
            "Gasto nacional bruto (% del PIB)",
            "Ahorro bruto (% del PIB)",
            "Gasto militar (% del PIB)",
            "Gasto en investigación y desarrollo (% del PIB)",
        ],
        "Definición": [
            "Total de la deuda del gobierno central en relación al PIB.",
            "Total del gasto del gobierno en salud en relación al PIB.",
            "Total del gasto del gobierno en relación al PIB.",
            "Inversión extranjera neta recibida en relación al PIB.",
            "Tasa de crecimiento anual del PIB per cápita.",
            "PIB dividido por la población, medido en dólares actuals.",
            "PIB dividido por la población, medido en moneda local actual.",
            "Tasa de crecimiento anual del PIB.",
            "PIB per cápita ajustado por paridad de poder adquisitivo en dólares constantes de 2021.",
            "PIB per cápita ajustado por paridad de poder adquisitivo en dólares actuals.",
            "PIB dividido por la población empleada, ajustado por PPA en dólares constantes de 2021.",
            "Total del gasto gubernamental en educación en relación al PIB.",
            "Total del gasto del gobierno en bienes y servicios consumidos por el público en relación al PIB.",
            "Tasa de cambio anual en el deflactor del PIB, que mide la inflación general.",
            "Total de inversiones en activos fijos y cambios en inventarios en relación al PIB.",
            "Total de ahorro generado dentro de la economía en relación al PIB.",
            "Inversión en activos fijos en relación al PIB.",
            "Inversión en activos fijos por el sector privado en relación al PIB.",
            "Total del gasto en bienes y servicios dentro del país en relación al PIB.",
            "Total del ahorro nacional en relación al PIB.",
            "Total del gasto en defensa en relación al PIB.",
            "Total del gasto en I+D en relación al PIB.",
        ],
        "Propósito": [
            "Medir la carga de deuda del gobierno.",
            "Evaluar el gasto público en salud.",
            "Medir el nivel de gasto del gobierno.",
            "Evaluar la atracción de inversión extranjera.",
            "Medir el crecimiento económico por habitante.",
            "Comparar la riqueza promedio entre países.",
            "Medir la riqueza promedio en términos locales.",
            "Evaluar la expansión económica del país.",
            "Comparar el nivel de vida ajustado por costo de vida.",
            "Medir la riqueza promedio ajustada por costo de vida.",
            "Evaluar la productividad laboral.",
            "Medir la inversión pública en educación.",
            "Evaluar el gasto gubernamental en servicios públicos.",
            "Medir la inflación basada en el PIB.",
            "Medir la inversión en la economía.",
            "Evaluar la capacidad de ahorro nacional.",
            "Medir la inversión en infraestructura y equipos.",
            "Evaluar la inversión privada en la economía.",
            "Medir la demanda interna total.",
            "Evaluar la capacidad de ahorro del país.",
            "Medir la inversión en defensa nacional.",
            "Evaluar la inversión en innovación y tecnología.",
        ],
        "Importancia": [
            "Indica la sostenibilidad fiscal del gobierno.",
            "Refleja el compromiso del gobierno con la salud pública.",
            "Indica la eficiencia y alcance del gasto público.",
            "Señala la confianza internacional y potencial de crecimiento económico.",
            "Indica el desarrollo económico y aumento del nivel de vida.",
            "Refleja el bienestar económico de los ciudadanos.",
            "Permite la evaluación interna de la economía.",
            "Indica la salud y dinámica económica del país.",
            "Proporciona una comparación más realista del bienestar entre países.",
            "Facilita la comparación internacional de estándares de vida.",
            "Indica la eficiencia económica y productividad del trabajo.",
            "Refleja la prioridad del gobierno en el desarrollo educativo.",
            "Indica la implicación del gobierno en la economía y servicios públicos.",
            "Refleja la variación de precios de todos los bienes y servicios producidos.",
            "Indica el nivel de desarrollo y expansión de la capacidad productiva.",
            "Refleja la disponibilidad de recursos para inversión futura.",
            "Indica el crecimiento potencial de la capacidad productiva.",
            "Refleja la confianza del sector privado y su contribución al crecimiento.",
            "Indica la fortaleza del consumo y la inversión interna.",
            "Señala los recursos disponibles para inversión y crecimiento económico.",
            "Indica la prioridad del gobierno en seguridad y defensa.",
            "Refleja el compromiso con el progreso científico y tecnológico.",
        ],
    }

    df = pd.DataFrame(data)
    df = df.set_index("Nombre en inglés")
    return df


def social_guide():
    data = {
        "Nombre en inglés": [
            "Adolescents out of school (% of lower secondary school age)",
            "Current education expenditure, total (% of total expenditure in public institutions)",
            "Educational attainment, at least Bachelor's or equivalent, population 25+, total (%) (cumulative)",
            "Educational attainment, at least completed lower secondary, population 25+, total (%) (cumulative)",
            "Government expenditure on education, total (% of GDP)",
            "Government expenditure on education, total (% of government expenditure)",
            "Literacy rate, adult total (% of people ages 15 and above)",
            "Poverty headcount ratio at societal poverty line (% of population)",
            "Poverty headcount ratio at national poverty lines (% of population)",
            "Poverty headcount ratio at $2.15 a day (2017 PPP) (% of population)",
            "Multidimensional poverty headcount ratio (World Bank) (% of population)",
            "Share of youth not in education, employment or training, total (% of youth population)",
            "Unemployment, total (% of total labor force) (modeled ILO estimate)",
            "Unemployment, total (% of total labor force) (national estimate)",
            "Social contributions (% of revenue)",
        ],
        "Traducción": [
            "Adolescentes fuera de la escuela (% de la edad de la escuela secundaria inferior)",
            "Gasto actual en educación, total (% del gasto total en instituciones públicas)",
            "Logro educativo, al menos licenciatura o equivalente, población 25+, total (%) (acumulativo)",
            "Logro educativo, al menos secundaria completa, población 25+, total (%) (acumulativo)",
            "Gasto del gobierno en educación, total (% del PIB)",
            "Gasto del gobierno en educación, total (% del gasto gubernamental)",
            "Tasa de alfabetización, total de adultos (% de personas de 15 años y más)",
            "Tasa de pobreza según la línea de pobreza social (% de la población)",
            "Tasa de pobreza según las líneas de pobreza nacionales (% de la población)",
            "Tasa de pobreza según $2.15 al día (2017 PPA) (% de la población)",
            "Tasa de pobreza multidimensional (Banco Mundial) (% de la población)",
            "Proporción de jóvenes que no estudian, ni trabajan, ni reciben formación, total (% de la población juvenil)",
            "Desempleo, total (% de la fuerza laboral total) (estimación OIT modelada)",
            "Desempleo, total (% de la fuerza laboral total) (estimación nacional)",
            "Contribuciones sociales (% de los ingresos)",
        ],
        "Definición": [
            "Porcentaje de adolescentes de edad de secundaria inferior que no asisten a la escuela.",
            "Gasto actual en educación como porcentaje del gasto total en instituciones públicas.",
            "Porcentaje acumulado de la población de 25 años o más con al menos una licenciatura o equivalente.",
            "Porcentaje acumulado de la población de 25 años o más que ha completado al menos la educación secundaria inferior.",
            "Total del gasto gubernamental en educación en relación al PIB.",
            "Total del gasto gubernamental en educación en relación al gasto total del gobierno.",
            "Porcentaje de adultos de 15 años o más que pueden leer y escribir.",
            "Porcentaje de la población que vive por debajo de la línea de pobreza social.",
            "Porcentaje de la población que vive por debajo de las líneas de pobreza nacionales.",
            "Porcentaje de la población que vive con menos de $2.15 al día según la PPA de 2017.",
            "Porcentaje de la población que sufre pobreza multidimensional según el Banco Mundial.",
            "Porcentaje de jóvenes que no estudian, ni trabajan, ni reciben formación.",
            "Porcentaje de la fuerza laboral total que está desempleada según estimación modelada de la OIT.",
            "Porcentaje de la fuerza laboral total que está desempleada según estimación nacional.",
            "Porcentaje de los ingresos que proviene de contribuciones sociales.",
        ],
        "Propósito": [
            "Medir la exclusión educativa entre adolescentes.",
            "Evaluar la asignación de recursos actuals en educación.",
            "Medir el nivel educativo de la población adulta.",
            "Medir el logro educativo mínimo de la población adulta.",
            "Evaluar la inversión pública en educación.",
            "Medir la proporción del gasto total del gobierno dedicado a la educación.",
            "Medir el nivel de alfabetización entre adultos.",
            "Evaluar la proporción de población en pobreza social.",
            "Medir la proporción de población en pobreza según estándares nacionales.",
            "Evaluar la pobreza extrema en la población.",
            "Medir la proporción de población en pobreza multidimensional.",
            "Evaluar la proporción de jóvenes que no participan en actividades educativas o laborales.",
            "Medir la tasa de desempleo total según estimaciones internacionales.",
            "Medir la tasa de desempleo total según estimaciones nacionales.",
            "Evaluar la contribución de las contribuciones sociales a los ingresos totales.",
        ],
        "Importancia": [
            "Refleja el acceso y permanencia en la educación secundaria.",
            "Indica el nivel de apoyo financiero a la educación en instituciones públicas.",
            "Refleja el nivel educativo avanzado de la población adulta.",
            "Indica el nivel mínimo de educación completada por la población adulta.",
            "Refleja la prioridad del gobierno en el desarrollo educativo.",
            "Indica el compromiso del gobierno con la educación en su presupuesto total.",
            "Refleja el nivel de alfabetización y educación básica de los adultos.",
            "Indica el nivel de pobreza relativa en la sociedad.",
            "Refleja la pobreza según estándares locales y sus desafíos.",
            "Indica el nivel de pobreza extrema y la calidad de vida.",
            "Refleja múltiples dimensiones de la pobreza más allá del ingreso.",
            "Indica la integración de los jóvenes en el sistema educativo y laboral.",
            "Refleja la salud del mercado laboral según estándares internacionales.",
            "Refleja la salud del mercado laboral según estándares nacionales.",
            "Indica la relevancia de las contribuciones sociales en la financiación pública.",
        ],
    }

    df = pd.DataFrame(data)
    df = df.set_index("Nombre en inglés")
    return df
