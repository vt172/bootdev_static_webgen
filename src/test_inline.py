import unittest

from textnode import *
from inline import *

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

class Test_split_nodes_image(unittest.TestCase):
	def test_basic_link(self):
		node = TextNode(
			"This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
			TextType.TEXT,
		)
		results = split_nodes_image([node])
		expectations = [
			TextNode("This is text with a ", TextType.TEXT),
			TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
			TextNode(" and ", TextType.TEXT),
			TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
		]
		self.assertEqual(results,expectations)

	def test_nobefore_nospace(self):
		results = split_nodes_image([TextNode("![alt1](url1)![alt2](url2)",TextType.TEXT)])
		expectations = [
			TextNode("alt1", TextType.IMAGE, url="url1"),
			TextNode("alt2", TextType.IMAGE, url="url2")
		]
		self.assertEqual(results,expectations)

	def test_empty_TextNode(self):
		results = split_nodes_image([TextNode("",TextType.TEXT)])
		expectations = []
		self.assertEqual(results,expectations)

	def test_space_and_aftertext(self):
		results = split_nodes_image([TextNode("![a](url1) text ![b](url2) end", TextType.TEXT)])
		expectations = [
			TextNode("a", TextType.IMAGE, url="url1"),
			TextNode(" text ", TextType.TEXT),
			TextNode("b", TextType.IMAGE, url="url2"),
			TextNode(" end", TextType.TEXT)
		]
		self.assertEqual(results,expectations)
# Since the function for links is basically copy and paste of images I'm not testing it here.

class Test_text_to_textnode(unittest.TestCase):
	def example_case(self):
		text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
		results = text_to_textnode(text)
		expectations = [
			TextNode("This is ", TextType.TEXT),
			TextNode("text", TextType.BOLD),
			TextNode(" with an ", TextType.TEXT),
			TextNode("italic", TextType.ITALIC),
			TextNode(" word and a ", TextType.TEXT),
			TextNode("code block", TextType.CODE),
			TextNode(" and an ", TextType.TEXT),
			TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
			TextNode(" and a ", TextType.TEXT),
			TextNode("link", TextType.LINK, "https://boot.dev"),
		]
		self.assertEqual(results,expectations)

	def test_empty_string(self):
		results = text_to_textnode("")
		expectations = []
		self.assertEqual(results,expectations)

	def test_unmatched_demiter(self):
		text = "Text with `unmatched delimiter"
		with self.assertRaises(Exception):
			text_to_textnode(text)

	def test_empty_link(self):
		results = text_to_textnode("[]()")
		expectations = []
		self.assertEqual(results,expectations)

	def test_empty_image_link(self):
		results= text_to_textnode("![]()")
		expectations = []
		self.assertEqual(results,expectations)

	def test_adjacent(self):
		results = text_to_textnode("**bold**_italic_")
		expectations = [
			TextNode("bold", TextType.BOLD),
			TextNode("italic", TextType.ITALIC)
		]
		self.assertEqual(results,expectations)

	def test_special_character(self):
		results = text_to_textnode("[!](google.com)")
		expectations = [
			TextNode("!",TextType.LINK,url="google.com")
		]
		self.assertEqual(results,expectations)

