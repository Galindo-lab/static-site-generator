import os
import string
import json
import shutil

from pathlib import Path

import markdown


def is_public(name: str) -> bool:
    return name[0] != '-'


class Proyect():
    data: dict
    origin: str

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
        for section in self.sections:
            # Directorio de origen y destino del articulo
            origin_dir = Path(self.origin, section)

            # articulos en el directorio origen (secciones)
            for article in origin_dir.iterdir():
                if not is_public(article.name):
                    self.unpublish(section, article)
                    continue
                else:
                    self.publish(section, article)


    def publish(self, section: str, article_path: Path ):
        destiny = Path(self.destination, section,article_path.name)
        self.export_md2html(article_path, destiny)
        
                
    def unpublish(self,section: str,article_path: Path):
        # eliminar el primer '-'
        # https://stackoverflow.com/a/4945578
        name = article_path.name.lstrip("-")
        afile = Path(self.destination, section, name).with_suffix(".html")
        if afile.exists(): afile.unlink()
        

    def export_md2html(self, origin: Path, destiny: Path):
        destination = destiny.with_suffix(".html")
        md_text = origin.read_text()
        html_text = markdown.markdown(md_text)
        destination.write_text(html_text)
