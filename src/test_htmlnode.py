import unittest

from htmlnode import HTMLNode,LeafNode

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

if __name__ == "__main__":
	unittest.main()
