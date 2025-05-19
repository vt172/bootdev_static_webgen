from enum import Enum
from htmlnode import LeafNode


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return False
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


def textnode_to_htmlnode(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(tag=None, value=text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode(tag="b", value=text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode(tag="i", value=text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode(tag="code", value=text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode(
            tag="img", value="", props={"src": text_node.url, "alt": text_node.text}
        )
    else:
        raise Exception("Type unsupported.")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT or delimiter not in node.text:
            new_nodes.append(node)
            continue
        if node.text.count(delimiter) % 2 != 0:
            raise Exception("For every delimiter, there should be a matching delimiter") 
        if delimiter == "":
            raise Exception("A delimiter cannot be empty")
        if not isinstance(node,TextNode):
            raise Exception("This functions works with TextNode, please insert a list of TextNode instead")
        node_text_split = node.text.split(delimiter)

        in_delimiter = node_text_split[0] == ""

        for text in node_text_split:
            if in_delimiter and text:
                new_node = TextNode(text,text_type)
                in_delimiter = not in_delimiter
                new_nodes.append(new_node)

            elif not in_delimiter and text:
                new_node = TextNode(text,TextType.TEXT)
                in_delimiter = not in_delimiter
                new_nodes.append(new_node)
            elif not text:
                in_delimiter = not in_delimiter
                continue

def extract_markdown_images(text):
    pass

    return new_nodes