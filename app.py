import streamlit as st
from PIL import Image
import pandas as pd
import random
import unidecode

# Configuración de Streamlit para Moodle CSV Generator
st.set_page_config(
    page_title="Generador de CSV para Moodle",
    page_icon="📚",
    initial_sidebar_state='collapsed',
    menu_items={
        'Get Help': 'https://www.isabellaea.com',  # Actualiza con tu URL de ayuda
        'Report a bug': 'https://alexander.oviedo.isabellaea.com/',  # URL para reportar errores
        'About': ("Moodle CSV Generator es una herramienta diseñada para facilitar la generación "
                  "de archivos CSV compatibles con Moodle. Ideal para administradores de sistemas "
                  "educativos, profesores y personal técnico involucrado en la gestión de plataformas "
                  "educativas digitales.")
    }
)

# Carga y muestra el logo de la aplicación / Load and show the application logo
logo = Image.open('Moodle_CSV_Generator.png')
st.image(logo, width=250)

# Función para generar un password aleatorio de seis dígitos
def generar_password():
    return random.randint(100000, 999999)

# Función para limpiar el texto, eliminando tildes y reemplazando ñ por n
def limpiar_texto(texto):
    return unidecode.unidecode(texto)

# Función para transformar el nombre completo en los componentes necesarios
def transformar_nombre(nombre_completo, grado, dominio_email):
    partes_nombre = nombre_completo.split()
    username = ".".join(partes_nombre).lower()
    firstname = " ".join(partes_nombre[:2])
    lastname = " ".join(partes_nombre[2:])
    email = f"{username}{dominio_email}"
    course1 = f"PAV-{grado}"
    return [username, generar_password(), firstname, lastname, email, course1]

# Inicio de la aplicación Streamlit
st.title('Generador de Archivo Plano para Campus Virtual')

# Campo para ingresar el dominio del correo electrónico
dominio_email = st.text_input("Ingresa el dominio del correo electrónico:", value="@bosquesdeleon.com")

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

# Procesamiento de los datos cuando se presiona el botón
boton_generar_presionado = st.button("Generar Archivo Plano")
if boton_generar_presionado:
    if not dominio_email.strip():
        st.error("Por favor, ingresa el dominio del correo electrónico.")
    elif not datos_entrada:
        st.error("Por favor, ingresa los datos para generar el archivo.")
    else:
        datos_transformados = [transformar_nombre(limpiar_texto(nombre), grado, dominio_email) for nombre, grado in (e.split("...") for e in datos_entrada)]
        df_transformado = pd.DataFrame(datos_transformados, columns=['username', 'password', 'firstname', 'lastname', 'email', 'course1'])
        archivo_salida = "CampusVirtual.csv"
        df_transformado.to_csv(archivo_salida, index=False, sep=';')
        st.success("Archivo generado exitosamente!")
        st.download_button(label="Descargar Archivo", data=df_transformado.to_csv(index=False, sep=';'), file_name=archivo_salida, mime='text/csv')

st.sidebar.markdown('---')
st.sidebar.subheader('Creado por:')
st.sidebar.markdown('Alexander Oviedo Fadul')
st.sidebar.markdown("[GitHub](https://github.com/bladealex9848) | [Website](https://alexander.oviedo.isabellaea.com/) | [Instagram](https://www.instagram.com/alexander.oviedo.fadul) | [Twitter](https://twitter.com/alexanderofadul) | [Facebook](https://www.facebook.com/alexanderof/) | [WhatsApp](https://api.whatsapp.com/send?phone=573015930519&text=Hola%20!Quiero%20conversar%20contigo!%20)")