from enum import Enum
from htmlnode import LeafNode
import re


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
	return new_nodes


def extract_markdown_images(text):
	return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_link(text):
	return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_images(old_nodes):
	new_nodes = []

	# Inner recursive Function
	def recursive_split_images(text, images)
			# Base Case : images is a list of tuples. if empty, it means that there is 
			# no more images add therefore we reached to bottom of the recursion.
			if not images:
				return [TextNode(text,TextType.TEXT)]
			# Recursive Case
			else:
				# unpacking the first tuple
				alt_text, url = images[0]
				# splitting the text in 2, before the image and after
				split_nodes = node.text.split(f"![{alt_text}]({url})", 1)
				# assigning it
				before_image_text = split_nodes[0]
				after_image_text = split_nodes[1]	
				
				# no need to create a new textnode if the string is empty
				if before_image_text:
					before_image_node = TextNode(before_image_text,TextType.TEXT)
				# using the alt_text and url to create the node.
				image_node = TextNode(alt_text,TextType.IMAGE,url=url)
				# the recursive call, we are supposed to receive a list of nodes here
				return [before_image_node, image_node].extend(
						recursive_split_images(after_image_text,images[1:])
					)

	# Now looping through all the nodes
	for node in old_nodes:	
		if node.text_type != TextType.TEXT:
			new_nodes.append(node)
			continue
		if not isinstance(node,TextNode):
			raise Exception("This functions works with TextNode, please insert a list of TextNode instead")
			continue

		# We are using the helper function to extract a list of tuples containing text
		# and image link
		images = extract_markdown_images(node.text)

		# We extend the list with the results of the inner function
		new_nodes.extend(recursive_split_images(node.text, images))

	return new_nodes





	return new_nodes 

node = TextNode(
	"This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
    TextType.TEXT,
	)
split_nodes_images([node])
