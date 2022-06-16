
import markdown
import os

def list_articles():
    return os.listdir("./articles")

def markdown2html(file_name: str):
    with open(f'{file_name}.md', 'r') as f:
        text = f.read()
        html = markdown.markdown(text)

    with open(f'{file_name}.html', 'w') as f:
        f.write(html)
    
