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
		self.assertEqual(node1,node2)

	def test_image(self):
		node1 = textnode_to_htmlnode(TextNode("This is image",TextType.IMAGE,url="https://wallpapers.com/images/high/nyan-cat-1920-x-1080-background-1ldrgvod52e6vi0m.webp"))
		node2 = LeafNode(tag="img",value="",props={'src':"https://wallpapers.com/images/high/nyan-cat-1920-x-1080-background-1ldrgvod52e6vi0m.webp", 'alt':"This is image"})
		self.assertEqual(node1,node2)

class Test_split_nodes_delimiter(unittest.TestCase):
	def test_one_delimiter(self):
		nodes1 = [
			TextNode("Text with ",TextType.TEXT),
			TextNode("code",TextType.CODE)
		]
		nodes2 = split_nodes_delimiter([TextNode("Text with `code`",TextType.TEXT)],"`",TextType.CODE)
		self.assertEqual(nodes1,nodes2)

	def test_doublechar_delimiter(self):
		nodes1 = [
			TextNode("Text with ", TextType.TEXT),
			TextNode("bold", TextType.BOLD)
		]
		nodes2 = split_nodes_delimiter([TextNode("Text with **bold**",TextType.TEXT)],"**",TextType.BOLD)
		self.assertEqual(nodes1,nodes2)

	def test_multiple_nodes(self):
		nodes = [
			TextNode("Text with `code`", TextType.TEXT),
			TextNode("Text with **bold**", TextType.TEXT)
		]
		nodes1 = [
			TextNode("Text with ", TextType.TEXT),
			TextNode("code", TextType.CODE),
			TextNode("Text with **bold**", TextType.TEXT),
		]
		nodes2 = split_nodes_delimiter(nodes,"`",TextType.CODE)
		self.assertEqual(nodes1,nodes2)

	def test_not_text(self):
		nodes1 = [TextNode("Bold Text", TextType.BOLD)]
		nodes2 = split_nodes_delimiter([TextNode("Bold Text",TextType.BOLD)],"",TextType.BOLD)
		self.assertEqual(nodes1,nodes2)

	def test_unmatched_delimiter(self):
		nodes = [TextNode("Text with `code inse", TextType.TEXT)]
		self.assertRaises(Exception, split_nodes_delimiter, nodes, "`", TextType.CODE)	

	def test_empty_delimiter(self):
		nodes = [TextNode("Text with `code` inside", TextType.TEXT)]
		self.assertRaises(Exception, split_nodes_delimiter, nodes, "", TextType.CODE)

	def test_not_TextNode(self):
		nodes = [LeafNode("code","Text with `code` inside")]
		self.assertRaises(Exception, split_nodes_delimiter, nodes, "`", TextType.CODE)

class Test_extract_markdown_images(unittest.TestCase):
	def test_basic_images(self):
		results = extract_markdown_images("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")
		expectations = [('rick roll', 'https://i.imgur.com/aKaOqIh.gif'), ('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg')]                                                                                                                                                                
		self.assertEqual(results,expectations)
	# not doing more tests because it was in he solution

class Test_extract_markdwon_link(unittest.TestCase):
	def test_basic_link(self):
		results = extract_markdown_link("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")
		expectations = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
		self.assertEqual(results,expectations)

if __name__ == "__main__":
	unittest.main()
