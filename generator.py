
import string
import json
import shutil
import pdb

from string import Template
from pathlib import Path

import markdown

base_directory = Path("content/")
publishing_directory = Path("site/")
template_directory = Path("templates/")


def list_md_files(directory: Path) -> list:
    """
    Iterar el directorio base para extraer los archivos '.md'
    """
    return [diir for diir in base_directory.glob("**/*.md")]


def publish_file(input_file: Path) -> Path:
    # eliminar el directorio base
    foo = input_file.relative_to(base_directory)
    # archivo equivalente en publishing_directory
    output_file = publishing_directory / foo.with_suffix(".html")
    return output_file


def load_template(name: str) -> Template:
    # file_name = Path(name).with_suffix(".html")
    template = template_directory / f"{name}.html"
    return Template(template.read_text())
    

def create_dirs():
    for diir in list_md_files(base_directory):
        folder = publish_file(diir).parent
        folder.mkdir(exist_ok=True)
        

def extract_meta(input_file: Path) -> dict: 
    """
    Extraer los metadatos de el documento.
    """
    md = markdown.Markdown(extensions=['meta'])
    file_path = str(input_file.resolve()) # Path to string
    md_meta = md.convertFile(file_path).Meta
    return {k:v[0] for (k,v) in md_meta.items() }
    

def export_file(input_file: Path):
    """
    Aplicar la plantilla y escribir el archivo '.html'
    """
    output_file = publish_file(input_file)
    md = markdown.Markdown(extensions=['meta'])

    meta = extract_meta(input_file)
    md_text = input_file.read_text()
    html_text = md.convert(md_text)

    template_name = meta["template"] if "template" in meta else "default"
    template = load_template(template_name)
    
    output_file.write_text(template.substitute({
        "date" : meta["date"],
        "title" : meta["title"],
        "author" : meta["authors"],
        "content" : html_text
    }))
    
    

def export_files():
    for filee in list_md_files(base_directory):
        export_file(filee)
        


print(" TEST ")
create_dirs()
export_files()
print("")
