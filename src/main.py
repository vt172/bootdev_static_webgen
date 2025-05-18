from textnode import *
from htmlnode import *


def main():
    result = TextNode("This is some anchor text", "link", "https://google.com")
    print(f"...{result}")
    print(f"...{text_node_to_html_node(result)}")


if __name__ == "__main__":
    main()
