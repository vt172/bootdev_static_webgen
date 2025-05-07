import unittest

from htmlnode import HTMLNode,LeafNode,ParentNode

class TestHTMLNode(unittest.TestCase):
	def test_no_arguments(self):
		node = HTMLNode()
		node2 = HTMLNode(None,None,None,None)
		self.assertEqual(node, node2)

	def test_all_arguments(self):
		node = HTMLNode("tag","value",["element1","element2"],{"key":"value"})
		node2 = HTMLNode("tag","value",["element1","element2"],{"key":"value"})
		self.assertEqual(node,node2)

	def test_diff(self):
		node = HTMLNode("tag","value",["element1","element2"],{"key":"value"})
		node2 = HTMLNode("tag2","value",["element1","element2"],{"key":"value"})
		node3 = HTMLNode("tag","value2",["element1","element2"],{"key":"value"})
		node4 = HTMLNode("tag","value",["element3","element4"],{"key":"value"})
		node5 = HTMLNode("tag","value",["element1","element2"],{"key2":"value2"})
		self.assertNotEqual(node,node2)
		self.assertNotEqual(node,node3)
		self.assertNotEqual(node,node4)
		self.assertNotEqual(node,node5)

class TestLeafNode(unittest.TestCase):
	def test_leaf_to_html_p(self):
		node = LeafNode("p", "Hello, world!")
		self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

	def test_leaf_to_html_link(self):
		node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
		self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

	def test_no_p(self):
		node = LeafNode(None,"Something")
		self.assertEqual(node.to_html(), "Something")

class TestParentNode(unittest.TestCase):
	def test_to_html_with_children(self):
		child_node = LeafNode("span", "child")
		parent_node = ParentNode("div", [child_node])
		self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

	def test_to_html_with_grandchildren(self):
		grandchild_node = LeafNode("b", "grandchild")
		child_node = ParentNode("span", [grandchild_node])
		parent_node = ParentNode("div", [child_node])
		self.assertEqual(
			parent_node.to_html(),
			"<div><span><b>grandchild</b></span></div>",
		)

	def test_to_html_many_children(self):
		node = ParentNode(
			"p",
			[
				LeafNode("b", "Bold text"),
				LeafNode(None, "Normal text"),
				LeafNode("i", "italic text"),
				LeafNode(None, "Normal text"),
			],
		)
		self.assertEqual(
			node.to_html(),
			"<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
		)

	def test_headings(self):
		node = ParentNode(
			"h2",
			[
				LeafNode("b", "Bold text"),
				LeafNode(None, "Normal text"),
				LeafNode("i", "italic text"),
				LeafNode(None, "Normal text"),
			],
		)
		self.assertEqual(
			node.to_html(),
			"<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
		)


if __name__ == "__main__":
	unittest.main()
