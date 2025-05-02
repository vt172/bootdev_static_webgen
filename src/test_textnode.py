import unittest

from textnode import TextNode, TextType

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

if __name__ == "__main__":
    unittest.main()
