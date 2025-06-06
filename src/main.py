from textnode import *
from htmlnode import *
from blocks import *
import sys, shutil, os
from pathlib import Path
from datetime import datetime


global ignore 
ignore = (
    ".DS_Store"
)

global current_path 
global static_path
global public_path
current_path = Path.cwd()
static_path = current_path / "static"
public_path = current_path / "public"


def copy_static():
    print(f"==== {public_path}")

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
        return

    def get_static_items(path):
        static_items = []
        for item in path.iterdir():
            if item.is_file() and item.name not in ignore:
                static_items.append(item)
            elif item.is_dir() and item.name not in ignore:
                static_items.append(item)
                static_items.extend(get_static_items(item))
        return static_items


    def create_folders(items):
        for folder in folders:
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

    delete_public(public_path)

    static_items = get_static_items(static_path)
    folders = (folder for folder in static_items if folder.is_dir())
    files = (file for file in static_items if file.is_file())

    create_folders(folders)
    copy_items(files)

    return static_items

def extract_title(md):
    title = re.findall(r"^#\ .*", md)
    if title:
        return title[0][2:].strip()
    else:
        raise Exception(f"No title has been found\nFile:\n{md}")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}.")

    with from_path.open() as f: 
        md = f.read()
    with template_path.open() as f:
        template = f.read()

    content = markdown_to_html(md).to_html()
    title = extract_title(md)

    new_html = template.replace("{{ Title }}", title)
    new_html = new_html.replace("{{ Content }}", content)

    dest_path.touch()
    with open(dest_path, 'w') as f:
        f.write(new_html)



def main():
    copy_static()
    from_path = public_path / "content" / "index.md"
    template_path = current_path / "template.html"
    dest_path = public_path / "index.html"



    generate_page(from_path,template_path,dest_path)


if __name__ == "__main__":
    main()
