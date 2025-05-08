from textnode import *
from htmlnode import *
from enum import Enum

# text node to html function.
# It should handle each type of the TextType enum. If it gets a TextNode that is none of those types, it should raise an exception. Otherwise, it should return a new LeafNode object.
#    TextType.TEXT: This should return a LeafNode with no tag, just a raw text value.
#    TextType.BOLD: This should return a LeafNode with a "b" tag and the text
#    TextType.ITALIC: "i" tag, text
#    TextType.CODE: "code" tag, text
#    TextType.LINK: "a" tag, anchor text, and "href" prop
#    TextType.IMAGE: "img" tag, empty string value, "src" and "alt" props ("src" is the image URL, "alt" is the alt text)
def text_node_to_html_node(text_node):
	if text_node.text_type == TextType.TEXT.value:
		return LeafNode(tag=None,value=text_node.text)
	elif text_node.text_type == TextType.BOLD.value:
		return LeafNode(tag="b",value=text_node.text)
	elif text_node.text_type == TextType.ITALIC.value:
		return LeafNode(tag="i",value=text_node.text)
	elif text_node.text_type == TextType.CODE.value:
		return LeafNode(tag="code",value=text_node.text)
	elif text_node.text_type == TextType.LINK.value:
		return LeafNode(tag="a",value=text_node.text,props={"href": text_node.url})
	elif text_node.text_type == TextType.IMAGE.value:
		return LeafNode(tag='img',value='',{'src': text_node.url,'alt': text_node.value})
	else:
		raise Exception("Type unsupported")

def main():
	result = TextNode("This is some anchor text","link","https://google.com")
	print(f"...{result}")
	print(f"...{text_node_to_html_node(result)}")

if __name__ == "__main__":
	main()
