# import os
import string
import json
import shutil
import pdb

from string import Template
from pathlib import Path

import markdown

base_directory = Path("content/")
publishing_directory = Path("site/")
md = markdown.Markdown(extensions=['meta'])


def list_md_files(directory: Path) -> list:
    """
    Iterar el directorio base para extraer los archivos '.md'
    """
    return [diir for diir in base_directory.glob("**/*.md")]


def create_dirs():
    """
    Crear los directorios necesarios para los archivos.
    """
    for diir in list_md_files(base_directory):
        # eliminar el directorio base
        foo = diir.relative_to(base_directory)
        # directorio equivalente en publishing_directory
        folder = publishing_directory / foo.parent
        # crear el directorio si no existe
        folder.mkdir(exist_ok=True)


def extract(input_file: Path):
    """
    Extraer el texto en formato markdown y los metadatos de el 
    documento.
    """
    md_text = input_file.read_text()
    md_obj = md.convert(md_text)


def export(input_file: Path, output_file: Path):
    # ::clown emoji::
    outp = str(output_file.resolve())
    inpu = str(input_file.resolve())
    md_obj = md.convertFile(inpu, output=outp)
    return md_obj.Meta


def export_files():
    for filee in list_md_files(base_directory):
        # eliminar el directorio base
        foo = filee.relative_to(base_directory)
        # archivo equivalente en publishing_directory
        output = publishing_directory / foo


print(" ")
create_dirs()
# for txt_path in base_directory.glob("**/*.md"):
#     print(txt_path)

# md = markdown.Markdown(extensions = ['meta'])
# html = md.convertFile("./content/test1/-22-22-22.md")
# meta = md.Meta
