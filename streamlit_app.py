import streamlit as st

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from PIL import Image

# DATOS
MESES = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
ESTILOS_GRAFICOS = ["default", "seaborn-whitegrid", "ggplot", "seaborn-dark", "fivethirtyeight"]
TIPOS_DE_GRAFICOS = ["Gráfico de línea", "Gráfico de barras"]
FONTS = ["Arial", "Calibri", "Consolas", "Myriad Pro", "Tahoma", "Times New Roman", "Trebuchet MS", "Verdana"]
FONT_WEIGHT = ["normal", "bold"]
FONT_STYLE = ["normal", "italic"]
COLOR_PALETTE = ["", "Set1", "Set2", "Paired", "pastel", "RdYlBu", "RdYlGn", "BrBG", "Spectral", "rocket"]

DATOS = {"Inflación": {"nombre_archivo": {"Anual": "data/inflación_anual.xlsx", "Mensual": "data/inflación_mensual.xlsx"},
                    "períodos": {"Anual": list(range(2017, 2023)), "Mensual": MESES},
                    "fuente": "Datosmacro.com (2022)",
                    "nombre_columnas": {"Anual": "año", "Mensual": "mes"}},
     "PBI (en USD)": {"nombre_archivo": {"Anual": "data/pbi.xlsx"}, 
                    "períodos": {"Anual": list(range(2016, 2023))},
                    "fuente": "Banco Mundial (2022)",
                    "nombre_columnas": {"Anual": "año"}}
}

DATOS_MACROECONOMICOS = [""]+[dato for dato in DATOS.keys()]

# FUNCIÓN PARA LEER EL ARCHIVO
@st.cache
def data(archivo):
     """Lee el archivo de Excel correspondiente al dato que se quiere graficar."""
     return pd.read_excel(archivo)

# FUNCIÓN PARA FILTRAR EL DATAFRAME
@st.cache
def dataframe_filtrado(dato, tipo_periodo, periodo_anual = None, periodo_mensual = None):
     """Función destinada a filtrar el DataFrame de acuerdo a las especificaciones del usuario."""

     dato_macroeconomico_dic = DATOS.get(dato)
     df = data(dato_macroeconomico_dic.get("nombre_archivo").get(tipo_periodo))

     if tipo_periodo == "Mensual":
          df_filtrado = df[(df["año"].isin(periodo_anual)) & (df["mes"].isin(periodo_mensual))]
     else:
          df_filtrado = df[(df["año"].isin(periodo_anual))]

     return df_filtrado

# FUNCIÓN PARA GRAFICAR LOS DATOS
def graficar_datos(df, dato_grafico, periodo_grafico, anios_sidebar,
               grafico_tipo, grafico_width, grafico_height, grafico_estilo, grafico_color, grafico_palette, grafico_line_width,
               titulo, titulo_font, titulo_font_size, titulo_font_weight, titulo_font_style, titulo_alineacion, titulo_font_color, 
               ejes_titulo_eje_x, ejes_titulo_eje_y, ejes_font, ejes_font_size, ejes_font_color):
     """Función destinada a graficar los datos de acuerdo a las especificaciones del usuario."""

     # Variables a utilizar luego en la función.
     TIPOS_DE_GRAFICOS_A_SNS = {"Gráfico de línea": "lineplot",
                              "Gráfico de barras": "barplot"}
     POSICION_TITULO = {"Centro": "center", "Izquierda": "left", "Derecha": "right"}

     columna_X = DATOS.get(dato_grafico).get("nombre_columnas").get(periodo_grafico)
     cant_colores_palette = len(anios_sidebar)

     # Estilo del gráfico
     eval(f"plt.style.use('{grafico_estilo}')")

     # Crea la figura con un tamaño especificado por el usuario
     fig, ax = plt.subplots(1, 1, figsize=(grafico_width, grafico_height))

     # Condiciones para graficar
     general = f"data=df, x='{columna_X}', y='total'"
     especifico_lineplot = f"lw={grafico_line_width}, marker='o'"
     especifico_hue = f"hue='año'"
     especifico_color = f"color='{grafico_color}'" 
     especifico_palette = f"palette=sns.color_palette('{grafico_palette}', {cant_colores_palette})"

     if periodo_grafico == "Anual":
          # Si es gráfico de barras
          if grafico_tipo == "Gráfico de barras":
               if grafico_palette:
                    graficar = ", ".join([general, especifico_palette])
               else:
                    graficar = ", ".join([general, especifico_color])
          # Si es gráfico de línea
          else: 
               graficar = ", ".join([general, especifico_lineplot, especifico_color])

     elif periodo_grafico == "Mensual":
          # Si es gráfico de barras
          if grafico_tipo == "Gráfico de barras":
               if grafico_palette:
                    graficar = ", ".join([general, especifico_hue, especifico_palette])
               else:
                    graficar = ", ".join([general, especifico_hue, especifico_color])
          # Si es gráfico de línea
          else:
               if grafico_palette:
                    graficar = ", ".join([general, especifico_hue, especifico_lineplot, especifico_palette])
               else:
                    graficar = ", ".join([general, especifico_hue, especifico_lineplot, especifico_color])

     
     # Realiza el gráfico
     ax = eval(f'sns.{TIPOS_DE_GRAFICOS_A_SNS.get(grafico_tipo)}({graficar})')

     # Título
     ax.set_title(titulo, pad=15, fontdict={"fontname": titulo_font}, size=titulo_font_size, fontweight=titulo_font_weight, fontstyle=titulo_font_style, loc=POSICION_TITULO.get(titulo_alineacion), color=titulo_font_color)
     
     # Eje x
     ax.set_xlabel(xlabel=ejes_titulo_eje_x, size=ejes_font_size, color=ejes_font_color, fontdict={"fontname": ejes_font})
     
     # Eje y
     ax.set_ylabel(ylabel=ejes_titulo_eje_y, size=ejes_font_size, color=ejes_font_color, fontdict={"fontname": ejes_font})

     # Fuente de los ticks de ambos ejes y del legend (coincide con los títulos de los ejes)
     plt.xticks(fontname=ejes_font)
     plt.yticks(fontname=ejes_font)

     # Legend sólo para los gráficos mensuales. Modifica el título del legend y la fuente.
     if periodo_grafico == "Mensual":
          plt.legend(title="Años", prop=ejes_font)

     # Fuente de los datos - Posición fija en función del ancho/alto del gráfico así no se supoerpone con el eje X.
     # ax.text(x=-0.45, y=-0.7, s=f'Fuente: {DATOS.get(dato_grafico).get("fuente")}', size=10, fontdict={"fontname": ejes_font})

     return fig

# CONTENIDO
st.info("Si visualizás tu gráfico con una calidad baja, no te preocupes! 😉 Es la forma en la que la aplicación renderiza la imagen. Al descargarla vas a tener la máxima calidad.")
st.header("Tu gráfico personalizado:")

## SIDEBAR
logo = Image.open("img/logo_background.png")
st.sidebar.image(logo, width=200)

st.sidebar.subheader("Datos")
dato_grafico = st.sidebar.selectbox("Datos del gráfico:", DATOS_MACROECONOMICOS)

dato_grafico_dic = DATOS.get(dato_grafico, None)

### SIDEBAR - AL ELEGIR UN DATO MACROECONÓMICO VÁLIDO
if dato_grafico_dic:
     periodo_grafico = st.sidebar.selectbox("Período:", dato_grafico_dic.get("períodos"))

     anios_sidebar = st.sidebar.multiselect("Año", dato_grafico_dic.get("períodos").get("Anual"), dato_grafico_dic.get("períodos").get("Anual"))

     if periodo_grafico == "Anual":
          meses_sidebar = st.sidebar.multiselect("Mes", [], disabled=True)
     else:
          meses_sidebar = st.sidebar.multiselect("Mes", dato_grafico_dic.get("períodos").get("Mensual"), dato_grafico_dic.get("períodos").get("Mensual"))

     st.sidebar.subheader("Gráfico")
     grafico_tipo = st.sidebar.selectbox("Tipo de gráfico:", TIPOS_DE_GRAFICOS)
     grafico_width = st.sidebar.slider("Ancho del gráfico", 1, 20, 7)
     grafico_height = st.sidebar.slider("Alto del gráfico", 1, 20, 4)
     grafico_estilo = st.sidebar.selectbox("Estilo del gráfico:", ESTILOS_GRAFICOS)
     grafico_color = st.sidebar.color_picker("Color del gráfico:")

     if not (periodo_grafico == "Anual" and grafico_tipo == "Gráfico de línea"):
          grafico_palette = st.sidebar.selectbox("Paleta de colores:", COLOR_PALETTE)
     else:
          grafico_palette = st.sidebar.selectbox("Paleta de colores:", COLOR_PALETTE, disabled=True)

     if grafico_tipo == "Gráfico de línea":
          grafico_line_width = st.sidebar.slider("Ancho de la línea", 0.5, 5.0, 1.0)
     else:
          grafico_line_width = st.sidebar.slider("Ancho de la línea", 0.5, 5.0, 1.0, disabled=True)


     st.sidebar.subheader("Título")
     titulo = st.sidebar.text_input("Título:")
     titulo_font = st.sidebar.selectbox("Fuente:", FONTS)
     titulo_font_size = st.sidebar.slider("Tamaño", 10, 25, 15)
     titulo_font_weight = st.sidebar.selectbox("Font-weight:", FONT_WEIGHT)
     titulo_font_style = st.sidebar.selectbox("Font-style:", FONT_STYLE)
     titulo_alineacion = st.sidebar.selectbox("Alineación:", ["Centro", "Izquierda", "Derecha"])
     titulo_font_color = st.sidebar.color_picker("Color:")

     st.sidebar.subheader("Ejes")
     ejes_titulo_eje_x = st.sidebar.text_input("Título - eje X:")
     ejes_titulo_eje_y = st.sidebar.text_input("Título - eje Y:")
     ejes_font = st.sidebar.selectbox("Font:", FONTS)
     ejes_font_size = st.sidebar.slider("Tamaño:", 5, 20, 10)
     ejes_font_color = st.sidebar.color_picker("Color del títulos de los ejes:")


     ## GRÁFICO 
     df_filtrado = dataframe_filtrado(dato = dato_grafico, tipo_periodo = periodo_grafico, periodo_anual = anios_sidebar, periodo_mensual = meses_sidebar)

     fig = graficar_datos(df_filtrado, dato_grafico, periodo_grafico, anios_sidebar,
               grafico_tipo, grafico_width, grafico_height, grafico_estilo, grafico_color, grafico_palette, grafico_line_width,
               titulo, titulo_font, titulo_font_size, titulo_font_weight, titulo_font_style, titulo_alineacion, titulo_font_color, 
               ejes_titulo_eje_x, ejes_titulo_eje_y, ejes_font, ejes_font_size, ejes_font_color)

     st.pyplot(fig)

     ## DESCARGAR GRÁFICO
     nombre_archivo = "arplot.png"
     plt.savefig(nombre_archivo)
     with open(nombre_archivo, "rb") as img:
          btn = st.download_button(label="Descargar gráfico", data=img, file_name=nombre_archivo, mime="image/png")
