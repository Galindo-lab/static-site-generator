import os
import string
import json
import shutil

from string import Template
from pathlib import Path

import markdown







class Article():
    name: str
    section: str
    origin_path: Path
    destination_path: Path

    def __init__(self, origin: str, destination: str, section: str, name: str):
        # ningun archivo con '-' debe existir en el directorio de salida,
        # recuerda '-' al inicio del nombre del archivo siginifica que el
        # articulo no esta publicado
        # 
        # origen: https://stackoverflow.com/a/4945578
        self.name = name.lstrip("-")
        self.section = section
        self.origin_path = Path(origin, section, name).with_suffix(".md")
        self.destination_path = Path(destination, section,self.name).with_suffix(".html")

    def template_data(self, content: str) -> dict:
        """
        separar el nombre del archivo en sus componentes
        """
        keys = ["date", "title", "author", "content"]
        values = self.name.split("-")
        values.append(content)
        data = dict(zip(keys, values))
        
        return data

    def load_template(self) -> Template:
        default = Path("templates", "default").with_suffix(".html")
        template = Path("templates", self.section).with_suffix(".html")
        if not template.exists():
            return Template(default.read_text())

        return Template(template.read_text())
        
    def publish(self):
        """
        crear el archivo .html del articulo
        """
        md_text = self.origin_path.read_text()
        html_text = markdown.markdown(md_text)
        template = self.load_template()
        output = template.substitute(self.template_data(html_text))
        
        self.destination_path.write_text(output)

    def unpublish(self):
        """
        eliminar archivo .html del articulo
        """
        if self.destination_path.exists():
            self.destination_path.unlink()

    def is_published(self) -> bool:
        """
        Revisar si tiene el caracter '-' al inicio del 
        nombre
        """
        return self.origin_path.name[0] != '-'




















class Proyect():

    def __init__(self):
        self.load_data()
        self.update_folders()
        self.update_files()

    def load_data(self):
        with open("proyect.json") as json_file:
            self.data = json.load(json_file)

        self.destination = self.data["outputFolder"]
        self.origin = self.data["inputFolder"]
        self.sections = self.data["published-sections"]
        self.unpublished = self.data["unpublished-sections"]

    def update_folders(self):
        """
        Crea todos los directorios requeridos para trabajar los 
        el proyecto, si se despublica una seccion se elimina
        el directorio 
        """
        
        # eliminar folders de secciones despublicadas
        for section in self.unpublished:
            directory = Path(self.destination, section)
            if directory.exists():
                shutil.rmtree(directory)

        # crear los folders de las capetas publicadas
        for section in self.sections:
            directory = Path(self.destination, section)
            directory.mkdir(exist_ok=True)

    def update_files(self):
        """
        Actualiza los archivos html, si cambia su contenido 
        actualiza el archivo y si se despublica se elimina.
        """
        for section in self.sections:
            section_path = Path(self.origin, section)
            for article_path in section_path.glob("*.md"):
                article = Article(self.origin, self.destination,section,
                                  article_path.name)
                
                if not article.is_published():
                    article.unpublish()
                else:
                    article.publish()
