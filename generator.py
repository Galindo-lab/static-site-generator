import sys
from pathlib import Path

import jinja2
import markdown


# configuraciones
MD_ENCODING = "utf-8"

# con la extencion de metadatos
md = markdown.Markdown(extensions=['meta'])

# identificador de argumentos
SCRIPT_NAME = 0
FILE_PATH = 1

# numero minimo de argumentos
MIN_ARGS = 2

if __name__ == '__main__':
    if len(sys.argv) < MIN_ARGS:
        print("Archivo invalido")
        sys.exit(0)

    # Cargar los archivos
    # -------------------
    path = Path(sys.argv[FILE_PATH])

    if path.is_file() == False:
        # validar no si existe el archivo
        print(f'"{path}" no es un archivo')
        sys.exit(0)

    if path.suffix.lower() != ".md":
        # validar que es un archivo markdown
        print(f'"{path}" no es un archivo markdown')
        sys.exit(0)

    # cargar las plantillas
    # ---------------------
    template_loader = jinja2.FileSystemLoader("./templates")
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template("default.html")

    # convertir md a html
    # -------------------
    md_text = path.read_text(encoding=MD_ENCODING)
    html_text = md.convert(md_text)

    # crear el diccionario de carga
    # -----------------------------
    context = {"content": html_text}

    for key, value in md.Meta.items():
        context[key] = value[0] if len(value) < 2 else value

    # generar el documento html con plantilla
    # ---------------------------------------
    output_text = template.render(context)
    

    # escribir el archivo de salida
    # -----------------------------
    f = open(path.with_suffix(".html"), "r+")
    f.write(output_text)
    f.close()
