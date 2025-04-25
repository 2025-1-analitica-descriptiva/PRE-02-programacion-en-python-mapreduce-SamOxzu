"""Taller evaluable"""

# pylint: disable=broad-exception-raised

import fileinput
import glob
import os.path
import time
import string
from itertools import groupby


#
# Escriba la funcion que  genere n copias de los archivos de texto en la
# carpeta files/raw en la carpeta files/input. El nombre de los archivos
# generados debe ser el mismo que el de los archivos originales, pero con
# un sufijo que indique el número de copia. Por ejemplo, si el archivo
# original se llama text0.txt, el archivo generado se llamará text0_1.txt,
# text0_2.txt, etc.
#

def copy_raw_files_to_input_folder(n):
    """Funcion copy_files"""

    if os.path.exists("files/input"): # Verifica si el directorio existe
        for file in glob.glob("files/input/*"): # Busca todos los archivos en el directorio
            os.remove(file) # Elimina los archivos encontrados
        os.rmdir("files/input") # Elimina el directorio vacío (es necesario que esté vacío)
    os.makedirs("files/input") # Crea el directorio (indiferente de si existía o no)

    # Crea una lista con los nombres de los archivos en la carpeta files/raw
    # y empieza a recorrerlos.
    for file in glob.glob("files/raw/*"):
        # n veces
        for i in range(1, n + 1):
            # Abre el archivo original
            with open(file, "r", encoding="utf-8") as f:
                # Separa el nombre del archivo original y le añade el sufijo
                # que indica el número de copia.
                with open(
                    f"files/input/{os.path.basename(file).split('.')[0]}_{i}.txt",
                    "w",
                    encoding="utf-8",
                ) as f2:
                    f2.write(f.read()) # Copia el contenido del archivo original

#
# Escriba la función load_input que recive como parámetro un folder y retorna
# una lista de tuplas donde el primer elemento de cada tupla es el nombre del
# archivo y el segundo es una línea del archivo. La función convierte a tuplas
# todas las lineas de cada uno de los archivos. La función es genérica y debe
# leer todos los archivos de folder entregado como parámetro.
#
# Por ejemplo:
#   [
#     ('text0'.txt', 'Analytics is the discovery, inter ...'),
#     ('text0'.txt', 'in data. Especially valuable in ar...').
#     ...
#     ('text2.txt'. 'hypotheses.')
#   ]
#


def load_input(input_directory):
    """Funcion load_input"""

    # Inicializa una lista vacía
    sequence = []

    # Encuentra todos los archivos en el directorio de entrada
    files = glob.glob(f"{input_directory}/*")

    # Recorre cada archivo y cada línea de los archivos
    with fileinput.input(files=files) as f:
        for line in f:
            # Si la línea no está vacía, la agrega a la lista
            sequence.append((fileinput.filename(), line))
    # Devuelve la lista de tuplas
    return sequence


#
# Escriba la función line_preprocessing que recibe una lista de tuplas de la
# función anterior y retorna una lista de tuplas (clave, valor). Esta función
# realiza el preprocesamiento de las líneas de texto,
#
def line_preprocessing(sequence):
    """Line Preprocessing"""

    # Convierte cada línea a minúsculas y elimina los signos de puntuación
    # usando str.maketrans y str.translate.
    sequence = [
        (key, value.translate(str.maketrans("", "", string.punctuation)).lower())
        for key, value in sequence
    ]
    # Retorna el sequence transformado
    return sequence


#
# Escriba una función llamada maper que recibe una lista de tuplas de la
# función anterior y retorna una lista de tuplas (clave, valor). En este caso,
# la clave es cada palabra y el valor es 1, puesto que se está realizando un
# conteo.
#
#   [
#     ('Analytics', 1),
#     ('is', 1),
#     ...
#   ]
#

def mapper(sequence):
    """Mapper"""
    # Inicializa una especie de conteo de palabras
    # separando las palabras por espacios en blanco
    # e inicializa el conteo en 1. En tuplas.
    return [(word, 1) for _, value in sequence for word in value.split()]



#
# Escriba la función shuffle_and_sort que recibe la lista de tuplas entregada
# por el mapper, y retorna una lista con el mismo contenido ordenado por la
# clave.
#
#   [
#     ('Analytics', 1),
#     ('Analytics', 1),
#     ...
#   ]
#
def shuffle_and_sort(sequence):
    """Shuffle and Sort"""
    # Ordena la colección sequence por el primer elemento de cada tupla
    # (la clave) usando sorted y una función lambda como clave de ordenación.
    return sorted(sequence, key=lambda x: x[0])


#
# Escriba la función reducer, la cual recibe el resultado de shuffle_and_sort y
# reduce los valores asociados a cada clave sumandolos. Como resultado, por
# ejemplo, la reducción indica cuantas veces aparece la palabra analytics en el
# texto.
#
def reducer(sequence):
    """Reducer"""
    result = []
    # Agrupa la secuencia por la clave (palabra), la agrupación es group y la clave key
    for key, group in groupby(sequence, lambda x: x[0]):
        # Agrega a la lista result una tupla por cada palabra, acompañada
        # por cuántas veces aparece en su agrupación (sumando los valores).
        result.append((key, sum(value for _, value in group)))
    return result


#
# Escriba la función create_ouptput_directory que recibe un nombre de
# directorio y lo crea. Si el directorio existe, lo borra
#
def create_ouptput_directory(output_directory):
    """Create Output Directory"""

    if os.path.exists(output_directory): # Verifica si el directorio existe
        for file in glob.glob(f"{output_directory}/*"): # Busca todos los archivos en el directorio
            os.remove(file) # Elimina los archivos encontrados
        os.rmdir(output_directory) # Elimina el directorio vacío (es necesario que esté vacío)
    os.makedirs(output_directory) # Crea el directorio (indiferente de si existía o no)


#
# Escriba la función save_output, la cual almacena en un archivo de texto
# llamado part-00000 el resultado del reducer. El archivo debe ser guardado en
# el directorio entregado como parámetro, y que se creo en el paso anterior.
# Adicionalmente, el archivo debe contener una tupla por línea, donde el primer
# elemento es la clave y el segundo el valor. Los elementos de la tupla están
# separados por un tabulador.
#
def save_output(output_directory, sequence):
    """Save Output"""
    # Abre (y crea) el archivo part-00000 en modo escritura y codificación utf-8
    # en el directorio de salida entregado como parámetro.
    with open(f"{output_directory}/part-00000", "w", encoding="utf-8") as f:
        # Iteramos sobre la secuencia con cada pareja de clave y valor
        for key, value in sequence:
            # Escribimos en el archivo la clave y el valor separados por un tabulador
            # (tab) y un salto de línea (\n), el tabulador se usa para separar los
            # elementos de la tupla, ya que usar una coma o un espacio podría
            # generar confusión al leer el archivo (ya que podrían hacer parte de
            # la clave o el valor).
            f.write(f"{key}\t{value}\n")


#
# La siguiente función crea un archivo llamado _SUCCESS en el directorio
# entregado como parámetro.
#
def create_marker(output_directory):
    """Create Marker"""
    # Abre (y crea) el archivo _SUCCESS en modo escritura y codificación utf-8
    # en el directorio de salida entregado como parámetro.
    # Este archivo es un marcador (bandera) que indica que el trabajo se ha completado
    # correctamente.
    with open(f"{output_directory}/_SUCCESS", "w", encoding="utf-8") as f:
        f.write("")


#
# Escriba la función job, la cual orquesta las funciones anteriores.
#
def run_job(input_directory, output_directory):
    """Job"""
    sequence = load_input(input_directory)
    sequence = line_preprocessing(sequence)
    sequence = mapper(sequence)
    sequence = shuffle_and_sort(sequence)
    sequence = reducer(sequence)
    create_ouptput_directory(output_directory)
    save_output(output_directory, sequence)
    create_marker(output_directory)


if __name__ == "__main__":

    copy_raw_files_to_input_folder(n=1000)

    start_time = time.time()

    run_job(
        "files/input",
        "files/output",
    )

    end_time = time.time()
    print(f"Tiempo de ejecución: {end_time - start_time:.2f} segundos")
