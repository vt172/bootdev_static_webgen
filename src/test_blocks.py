import unittest
from blocks import *

class Test_markdown_to_blocks(unittest.TestCase): 

	# Simple Case
	def test_markdown_to_blocks(self):
		md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
		blocks = markdown_to_blocks(md)
		self.assertEqual(
			blocks,
			[
				"This is **bolded** paragraph",
				"This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
				"- This is a list\n- with items",
			],
		)


	def test_empty_blocks(self):
		md = """
This is a block





And another block
"""
		blocks = markdown_to_blocks(md)
		self.assertEqual(
			blocks,
			[
				"This is a block",
				"And another block"
			],
		)

class Test_block_to_blocktype(unittest.TestCase):
	# Easy cases
	def test_block_heading(self):
		block = "# This is a heading\n## Subheading\n###### Heading 6"
		results = block_to_blocktype(block)
		expectations = BlockType.HEADING
		self.assertEqual(results,expectations)
	def test_block_code(self):
		block = "```Code block```"
		results = block_to_blocktype(block)
		expectations = BlockType.CODE
		self.assertEqual(results,expectations)
	def test_block_quote(self):
		block = "> Code\n> Quote"
		results = block_to_blocktype(block)
		expectations = BlockType.QUOTE
		self.assertEqual(results,expectations)
	def test_block_ulist(self):
		block = "- test code\n- test code"
		results = block_to_blocktype(block)
		expectations = BlockType.ULIST
		self.assertEqual(results,expectations)
	def test_block_olist(self):
		block = "1. test\n2. test\n3. test"
		results = block_to_blocktype(block)
		expectations = BlockType.OLIST
		self.assertEqual(results,expectations)
	def test_block_paragraph(self):
		block = "Just a normal text paragraph"
		results = block_to_blocktype(block)
		expectations = BlockType.PARAGRAPH
		self.assertEqual(results,expectations)

	# Edge cases
	def test_multi_types(self):
		block = "- a list item\n1. something else\n- a list item"
		results = block_to_blocktype(block)
		expectations = BlockType.PARAGRAPH
		self.assertEqual(results,expectations)
	def test_empty_list_item(self):
		block = "- something\n - \n - test"
		results = block_to_blocktype(block)
		expectations = BlockType.ULIST
		self.assertEqual(results,expectations)
	def test_empty_quote_item(self):
		block = "> test\n>\n> test"
		results = block_to_blocktype(block)
		expectations = BlockType.QUOTE
		self.assertEqual(results,expectations)
	def test_empty_olist_item(self):
		block = "1. something\n 2. \n 3. test"
		results = block_to_blocktype(block)
		expectations = BlockType.OLIST
		self.assertEqual(results,expectations)
	def test_empty_block(self):
		block = ""
		results = block_to_blocktype(block)
		expectations = None
		self.assertEqual(results,expectations)
	def test_multidigit_olist(self):
		lines_list = []
		for i in range(1,101):
			line = f"{i}. list number {i}"
			lines_list.append(line)
		block = "\n".join(lines_list)
		results = block_to_blocktype(block)
		expectations = BlockType.OLIST
		self.assertEqual(results,expectations)

class Test_markdown_to_html(unittest.TestCase):
	def test_paragraphs(self):
	    md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

	    node = markdown_to_html(md)
	    html = node.to_html()
	    self.assertEqual(
	        html.strip("\n"),
	        "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
	    )
'''
	def test_codeblock(self):
	    md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

	    node = markdown_to_html(md)
	    html = node.to_html()
	    self.assertEqual(
	        html.strip("\n"),
	        "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
	    )

	def test_ulist(self):
		md = """
	- Something _should_ start
	- Another **will** follow
	"""
		node = markdown_to_html(md)
		html = node.to_html()
		self.assertEqual(
			html,
			"<div><ul><li>Something <i>should</i> start</li><li>Another <b>will</b> follow</li></ul></div>"
		)

	def test_olist(self):
		md = """
1. Something _should_ start
2. Another **will** follow
"""
		node = markdown_to_html(md)
		html = node.to_html()
		self.assertEqual(
			html,
			"<div><ol><li>Something <i>should</i> start</li><li>Another <b>will</b> follow</li></ol></div>"
		)

	def test_quote(self):
		md = """
> A Quote from a famous _philosopher_
> Who is this **person?**
"""
		node = markdown_to_html(md)
		html = node.to_html()
		self.assertEqual(
			html,
			"<div><blockquote>A Quote from a famous <i>philosopher</i>\nWho is this <b>person?</b></blockquote></div>"
		)

	def test_headings(self):
		md = """
# First

## Second

### Third

#### Fourth

##### Fith

###### Sixth
"""
		node = markdown_to_html(md)
		html = node.to_html()
		print("CACA")
		self.assertEqual(
			html,
			"<div><h1>First</h1><h2>Second</h2><h3>Third</h3><h4>Fourth</h4><h5>Fith</h5><h6>Sixth</h6></div>"
		)
'''