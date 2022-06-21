
import os, string, json
import markdown


def remove_suffix(file_name: str) -> str:
    """Elimina el suffijo del archivo"""
    return file_name.rsplit('.', 1)[0]


def remove_prefix(file_name: str) -> str:
    """Elimina el prefijo del archivo"""
    return file_name.rsplit('.', 1)[1]


def load(file_path: str) -> str:
    """carga el archivo"""
    with open(file_path, 'r') as f:
        text = f.read()
    return text

def save(file_path: str, content: str,):
    """Guarda el archivo"""
    with open(file_path, 'w') as f:
        f.write(content)

    


class Article():
    name: str
    origin_path: str
    destination_path: str
    data: dict

    def __init__(self, name: str, origin: str, destination: str):
        self.name = name
        self.origin_path = origin + "/" + name + ".md"
        self.destination_path = destination + "/" + name + ".html"
        self.data = Article._load_data(name)

    def is_published(self) -> bool:
        return self.name[0] == '-'

    @classmethod
    def _load_data(cls, name: str) -> dict:
        # significa que no esta publicado no vale la pena dividir el
        # string si no se van a usar las plantillas de todos modos
        if name[0] == "-": return {}
        data = name.rsplit('-')
        return {"date": data[0], "title": data[1], "author": data[2]}


class Section():
    name: str
    origin_path: str
    destination_path: str
    articles: list

    def __init__(self, name: str, origin: str, destination: str):
        org_path = origin + "/" + name
        des_path = destination + "/" + name
        self.name = name
        self.origin_path = org_path
        self.destination_path = des_path
        self.articles = Section._load_articles(org_path, des_path)

    @classmethod
    def _load_articles(cls, origin, destination) -> list:
        names = [remove_suffix(s) for s in os.listdir(origin)]
        return [Article(name, origin, destination) for name in names]


class Proyect():
    """Se encarga de la manipulacion del directorio output"""

    name: dict                  # nombre del proyecto
    origin: str                 # Ruta de origen el contenido
    destination: str            # Ruta donde se va a guardar 
    templates: str              # Ruta de las plantillas
    default: str                # Default Template
    published: list             # lista de secciones publicadas
    unpublished: list           # lista de secciones no publicadas

    
    def load_data(self, path: str):
        with open("proyect.json") as json_file:
            data = json.load(json_file)

        self.name = data["proyectName"]
        self.origin = data["inputFolder"]
        self.destination = data["outputFolder"]
        self.templates = data["templatesFolder"]
        self.default = data["defaultTemplate"]
        self.published = data["published-sections"]
        self.unpublished = data["unpublished-sections"]

    def generate_site(self):
        for sec_name in self.published:
            section = Section(sec_name, self.origin, self.destination)
            for article in section.articles:
                md_text = load(article.origin_path)
                save(article.destination_path, markdown.markdown(md_text))
            
    def update_sections(self):
        # elimina todos los directorios que ya no deben estar publicados
        for undir in self.unpublished:
            os.rmdir(self.destination + "/" + undir)

        # crea los directorios de cada seccion
        for pudir in self.published:
            os.makedirs(self.destination + "/" + pudir, exist_ok=True)
