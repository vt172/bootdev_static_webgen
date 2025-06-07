from textnode import *
from htmlnode import *
from blocks import *
from inline import *
import sys, shutil, os, re
from pathlib import Path
from datetime import datetime


global ignore 
ignore = (
    ".DS_Store"
)

global current_path 
global static_path
global public_path
global template_path
global content_path

current_path = Path.cwd()
static_path = current_path / "static"
public_path = current_path / "docs"
template_path = current_path / "template.html"
content_path = current_path / "content"

def get_items(path):
    static_items = []
    for item in path.iterdir():
        if item.is_file() and item.name not in ignore:
            static_items.append(item)
        elif item.is_dir() and item.name not in ignore:
            static_items.append(item)
            static_items.extend(get_items(item))
    return static_items


def delete_public(path):
    if not path.exists():
        print("Please create a public folder at the root of the project")
        return
    for item in path.iterdir():
        if item.is_file():
            print(f"Deleting file : {item}")
            item.unlink()
        if item.is_dir():
            print(f"Deleting folder : {item}")
            shutil.rmtree(item)

def copy_static():
    print(f"==== COPYING {static_path}")

    def create_folders(items):
        for folder in items:
            relative_to = folder.parent.relative_to(static_path)
            print(f"Creating : {public_path / relative_to / folder.name}")
            Path.mkdir(public_path / relative_to / folder.name)
        return

    def copy_items(items):
        for file in files:
            relative_to = file.parent.relative_to(static_path)
            print(f"Copying : {file} to public")
            shutil.copy(file, public_path / relative_to / file.name)
        return

    static_items = get_items(static_path)
    folders = [folder for folder in static_items if folder.is_dir()]
    files = [file for file in static_items if file.is_file()]

    create_folders(folders)
    copy_items(files)

    return static_items

def extract_title(md):
    title = re.findall(r"^#\ .*", md)
    if title:
        return title[0][2:].strip()
    else:
        raise Exception(f"No title has been found\nFile:\n{md}")

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}.\n\n")

    with from_path.open() as f: 
        md = f.read()
    with template_path.open() as f:
        template = f.read()

    title = extract_title(md)
    content = markdown_to_html(md).to_html() #### HERE IS THE PB

    new_html = template.replace("{{ Title }}", title)
    new_html = new_html.replace("{{ Content }}", content)

    new_html = new_html.replace('href="/"', f'href={basepath}')
    new_html = new_html.replace('src="/"', f'src={basepath}')

    dest_path.touch()
    with open(dest_path, 'w') as f:
        f.write(new_html)

    return

def create_htmlfolders(items):
    for folder in items:
        relative_to = folder.parent.relative_to(current_path / "content")
        print(f"Creating : {public_path / relative_to / folder.name}")
        Path.mkdir(public_path / relative_to / folder.name)
    return

def content_to_destination(file):
    relative_to = file.parent.relative_to(current_path / "content")
    htmlfile = file.stem + ".html"
    return public_path / relative_to / htmlfile

def generate_page_recursively(basepath):
    files = [file for file in get_items(content_path) if file.is_file()]
    folders = [folder for folder in get_items(content_path) if folder.is_dir()]
    create_htmlfolders(folders)
    for file in files:
        dest_path = content_to_destination(file)
        generate_page(file, template_path, dest_path, basepath)

def main():
    if len(sys.argv) >= 2:
        basepath = sys.argv[1]
    else:
        basepath = "/"
    delete_public(public_path)
    copy_static()
    generate_page_recursively(basepath)



if __name__ == "__main__":
    main()
