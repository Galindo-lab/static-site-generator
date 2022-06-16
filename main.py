import string
import markdown
import os


templates_folder = "./templates"
input_folder = "./content"
output_folder = "./site"
sections = [
    "test1", "test2", "test3"
]


def create_sections():
    for section in sections:
        os.makedirs(input_folder + "/" + section, exist_ok=True)
        os.makedirs(output_folder + "/" + section, exist_ok=True)


def file_names() -> list:
    """lista de archivos en el folder de entrada, solo nombres"""
    return os.listdir(input_folder)


def removesuffix(file_name: str) -> str:
    """Elimina el suffijo del archivo"""
    return file_name.rsplit('.', 1)[0]


def removeprefix(file_anme: str) -> str:
    """Elimina el prefijo del archivo"""
    return file_name.rsplit('.', 1)[1]


def filltemplate(template_path: str, param: dict) -> str:
    template = string.Template(load(template_path))
    return template.substitute(param)


def load(file_path: str) -> str:
    """carga el archivo"""
    with open(file_path, 'r') as f:
        text = f.read()
    return text


def save(content: str, file_path: str):
    """Guarda el archivo"""
    with open(file_path, 'w') as f:
        f.write(content)


def md2html(md_text: str):
    """Convertir archivo .md a .html"""
    return markdown.markdown(md_text)


def generate_site():
    for file_name in file_names():
        inputf = input_folder + "/" + removesuffix(file_name) + ".md"
        outputf = output_folder + "/" + removesuffix(file_name) + ".html"
        print(inputf)
        print(outputf)

        md_text = load(inputf)
        html_text = filltemplate(templates_folder + "/" + "root.html", {
            "title": removesuffix(file_name),
            "content": md2html(md_text)
        })

        save(html_text, outputf)


# def generate_site():
