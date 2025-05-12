import unittest

from textnode import *
from htmlnode import *

class TestTextNode(unittest.TestCase):
	def test_eq(self):
		node = TextNode("This is a text node", TextType.BOLD)
		node2 = TextNode("This is a text node", TextType.BOLD)
		self.assertEqual(node, node2)

	def test_typediff(self):
		node = TextNode("This is a text node", TextType.BOLD)
		node2 = TextNode("This is a text node", TextType.ITALIC)
		self.assertNotEqual(node,node2)

	def test_textdiff(self):
		node = TextNode("This is a text node", TextType.BOLD)
		node2 = TextNode("This is a different node", TextType.BOLD)
		self.assertNotEqual(node,node2)

	def test_urldiff(self):
		node = TextNode("This is a text node", TextType.BOLD,url='https://www.boot.dev/')
		node2 = TextNode("This is a text node", TextType.BOLD,url='https://docs.python.org/')
		self.assertNotEqual(node,node2)

	def test_url_none(self):
		node1 = TextNode("Same text", TextType.BOLD)  # url defaults to None
		node2 = TextNode("Same text", TextType.BOLD, None)  # explicitly None
		self.assertEqual(node1, node2)

		node3 = TextNode("Same text", TextType.BOLD, "https://example.com")
		self.assertNotEqual(node1,node3)

class Test_textnode_to_htmlnode(unittest.TestCase):
	def test_text(self):
		node1 = textnode_to_htmlnode(TextNode("This is text",TextType.TEXT))
		node2 = LeafNode(tag=None,value="This is text")
		self.assertEqual(node1,node2)

	def test_bold(self):
		node1 = textnode_to_htmlnode(TextNode("This is bold",TextType.BOLD))
		node2 = LeafNode(tag="b",value="This is bold")
		self.assertEqual(node1,node2)

	def test_italic(self):
		node1 = textnode_to_htmlnode(TextNode("This is italic",TextType.ITALIC))
		node2 = LeafNode(tag="i",value="This is italic")
		self.assertEqual(node1,node2)

	def test_code(self):
		node1 = textnode_to_htmlnode(TextNode("This is code",TextType.CODE))
		node2 = LeafNode(tag="code",value="This is code")
		self.assertEqual(node1,node2)

	def test_link(self):
		node1 = textnode_to_htmlnode(TextNode("This is link",TextType.LINK,url="https://google.com"))
		node2 = LeafNode(tag="a",value="This is link",props={"href": "https://google.com"})

	def test_image(self):
		node1 = textnode_to_htmlnode(TextNode("This is image",TextType.IMAGE,url="https://wallpapers.com/images/high/nyan-cat-1920-x-1080-background-1ldrgvod52e6vi0m.webp"))
		node2 = LeafNode(tag="img",value="",props={'src':"https://wallpapers.com/images/high/nyan-cat-1920-x-1080-background-1ldrgvod52e6vi0m.webp", 'alt':"This is image"})

if __name__ == "__main__":
	unittest.main()
