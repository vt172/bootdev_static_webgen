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


# text node to html function.
# It should handle each type of the TextType enum.
# If it gets a TextNode that is none of those types, it should raise an exception.
# Otherwise, it should return a new LeafNode object.
#    TextType.TEXT: This should return a LeafNode with no tag, just a raw text value
#    TextType.BOLD: This should return a LeafNode with a "b" tag and the text
#    TextType.ITALIC: "i" tag, text
#    TextType.CODE: "code" tag, text
#    TextType.LINK: "a" tag, anchor text, and "href" prop
#    TextType.IMAGE: "img" tag, empty string value, "src" and "alt" props
#       ("src" is the image URL, "alt" is the alt text)


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


# Now that we can convert TextNodes to HTMLNodes, we need to be able to create
# TextNodes from raw markdown strings.
# split_delimiter takes a list of nodes, a delimiter and its
# corresponding text_type
# it returns a new_nodes list of TextNodes. They have been 'split' using the
# delimiter. It doesn't support nested delimiters for now


def split_node_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT or delimiter not in node.text:
            new_nodes.append(node)
            continue
        node_text_split = node.text.split(delimiter)

        if node_text_split[0] == "":
            starts_with_delimiter = True
        else:
            starts_with_delimiter = False

        node_text_split = list(filter(lambda x: x.strip(),node_text_split))

        for i, text in enumerate(node_text_split,start=1):
            if starts_with_delimiter:
                if i % 2 == 0:
                    print("even: ", node)
                    node = TextNode(text, TextType.TEXT)
                else:
                    node = TextNode(text, text_type)
                    print("uneven: ", node)
            else:
                if i % 2 == 0:
                    node = TextNode(text, text_type)
                else:
                    node = TextNode(text, TextType.TEXT)
            new_nodes.append(node)
            # Ok the problem so far is that it doesn't
            # - handle unmatched delimiter
            # - still get confused when the first is a delimiter

    return new_nodes


node = TextNode("`code is a fantastic way of `expressing` yourself.`", TextType.TEXT)
new_nodes = split_node_delimiter([node], "`", TextType.CODE)
print(new_nodes)
