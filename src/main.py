from textnode import *
from htmlnode import *
from blocks import *
import sys, shutil, os
from pathlib import Path

def copy_static():
    current_path = Path.cwd()
    static_path = current_path / "static"
    public_path = current_path / "public"

    print(f"==== {public_path}")
    
    def delete_public(path):
        if not path.exists():
            print("Please create a public folder at the root of the project")
        for item in path.iterdir():
            if item.is_file():
                print(f"Deleting file : {item}")
                item.unlink()
            if item.is_dir():
                print(f"Deleting folder : {item}")
                shutil.rmtree(item)
        return

    delete_public(public_path)


def main():
    copy_static()


if __name__ == "__main__":
    main()
