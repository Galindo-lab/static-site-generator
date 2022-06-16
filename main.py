import markdown
import os

input_folder = "./content"
output_folder = "./output"


def file_names() -> list:
    """lista de archivos en el folder de entrada, solo nombres"""
    return os.listdir(input_folder)


def remocesuffux(file_name: str) -> str:
    """Elimina el suffijo del archivo"""
    return file_name.rsplit('.', 1)[0]


def md2html(inputf: str, outputf: str):
    """ Convertir archivo .md a .html """
    with open(inputf, 'r') as f:
        text = f.read()
        html = markdown.markdown(text)

    with open(outputf, 'w') as f:
        f.write(html)


def generate_site():
    for file_name in file_names():
        inputf = input_folder + "/" + remocesuffux(file_name) + ".md"
        outputf = output_folder + "/" + remocesuffux(file_name) + ".html"
        print(inputf)
        print(outputf)
        md2html(inputf, outputf)


# def generate_site():
