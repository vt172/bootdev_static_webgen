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
	def test_leadingspace_heading(self):
		block = " # This is a heading"
		results = block_to_blocktype(block)
		expectations = BlockType.HEADING
		self.assertEqual(results,expectations)