import os, string, json
import markdown

# Cargar el archivo proyect.json
with open("proyect.json") as json_file:
    data = json.load(json_file)

# Variables globales del proyecto
proyect_name = data["proyectName"]  # nombre del proyecto
input_dir = data["inputFolder"]  # directorio de entrada
output_dir = data["outputFolder"]  # directorio de salida
templates_dir = data["templatesFolder"]  # directorio de plantillas
default_template = data["defaultTemplate"]  # plantilla default
sections = data["sections"]  # secciones


def generate():
    input_dirs = input_path_list()  # Directorios de entrada
    output_dirs = output_path_list()  # Directorios de salida
    # input_files = input_files_paths()  #
    # output_files = output_files_paths()  #

    # crea los directorios de entrada si no existen
    # cada direcotrio correponde a una seccion
    for directory in input_dirs:
        make_dir(directory)

    # crea los directorios de salida si no existen
    for directory in output_dirs:
        make_dir(directory)

    for section in sections:
        # usar la plantilla default si no hay plantilla para
        # la seccion 
        template_path = template(section) if template_exist(
            section) else default_templat
        

def input_path_list() -> list:
    """Retorna la ruta de entrada para cada seccion del proyecto"""
    return [f"{input_dir}/{s}" for s in sections]


def output_path_list() -> list:
    """Retorna la ruta de salida para cada seccion del proyecto"""
    return [f"{output_dir}/{s}" for s in sections]


def make_dir(directory: list):
    """Crea un directorio"""
    os.makedirs(directory, exist_ok=True)


def template(section: str) -> str:
    return f"{templates_dir}/{section}.html"


def template_exist(section: str) -> bool:
    return os.path.exists(template(section))


def remove_suffix(file_name: str) -> str:
    """Elimina el suffijo del archivo"""
    return file_name.rsplit('.', 1)[0]


def remove_prefix(file_name: str) -> str:
    """Elimina el prefijo del archivo"""
    return file_name.rsplit('.', 1)[1]


def file_names(directory: str) -> list:
    """
    Lista de archivos en el directorio de entrada, solo
    nombres sin extensiones.
    """
    return list(map(remove_suffix, os.listdir(directory)))
