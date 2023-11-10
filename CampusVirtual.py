import streamlit as st
import pandas as pd
import random
import unidecode

# Función para generar un password aleatorio de seis dígitos
def generar_password():
    return random.randint(100000, 999999)

# Función para limpiar el texto, eliminando tildes y reemplazando ñ por n
def limpiar_texto(texto):
    return unidecode.unidecode(texto)

# Función para transformar el nombre completo en los componentes necesarios
def transformar_nombre(nombre_completo, grado):
    partes_nombre = nombre_completo.split()
    username = ".".join(partes_nombre).lower()
    firstname = " ".join(partes_nombre[:2])
    lastname = " ".join(partes_nombre[2:])
    email = f"{username}@bosquesdeleon.com"
    course1 = f"PAV-{grado}"
    return [username, generar_password(), firstname, lastname, email, course1]

# Inicio de la aplicación Streamlit
st.title('Generador de Archivo Plano para Campus Virtual')

# Opción de entrada: archivo de texto o texto directo
opcion = st.radio("Selecciona el método de entrada de datos:", ('Archivo de texto', 'Texto directo'))

datos_entrada = []

if opcion == 'Archivo de texto':
    archivo = st.file_uploader("Sube un archivo de texto con los datos", type=['txt'])
    if archivo is not None:
        # Leer el archivo como una lista de líneas
        datos_entrada = [line.strip() for line in archivo.getvalue().decode("utf-8").splitlines()]

elif opcion == 'Texto directo':
    datos_texto = st.text_area("Ingresa los datos directamente aquí:", height=250)
    if datos_texto:
        # Dividir el texto en líneas
        datos_entrada = datos_texto.split("\n")

if st.button("Generar Archivo Plano"):
    if datos_entrada:
        # Procesar los datos de entrada
        datos_transformados = [transformar_nombre(limpiar_texto(nombre), grado) for nombre, grado in (e.split("...") for e in datos_entrada)]
        df_transformado = pd.DataFrame(datos_transformados, columns=['username', 'password', 'firstname', 'lastname', 'email', 'course1'])

        # Guardar el DataFrame en un archivo CSV
        archivo_salida = "CampusVirtual.csv"
        df_transformado.to_csv(archivo_salida, index=False, sep=';')

        # Mostrar enlace de descarga
        st.success("Archivo generado exitosamente!")
        st.download_button(label="Descargar Archivo", data=df_transformado.to_csv(index=False, sep=';'), file_name=archivo_salida, mime='text/csv')
    else:
        st.error("Por favor, ingresa los datos para generar el archivo.")