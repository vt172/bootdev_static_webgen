from enum import Enum
from htmlnode import *
from inline import *
from textnode import *
import re

class BlockType(Enum):
	PARAGRAPH = "paragraph"
	HEADING = "heading"
	CODE = "code"
	QUOTE = "quote"
	ULIST = "unordered_list"
	OLIST = "ordered_list"

def markdown_to_blocks(text):
	blocks = text.split("\n\n")
	# this is a worth a comment : I'm using list comprehension (the []) to create the list. 
	# - block.strip() is the string stripped of whitespace
	# - this is added as I iterate through blocks : for block in blocks
	# - it is added if block.strip(), in python an empty string return false, so those are not added to the list
	blocks = [block.strip() for block in blocks if block.strip()]

	# Removes any leading or trailing \n
	for block in blocks:
		if block[0] == "\\" and block[1] == "\n":
			block = block[2:]
		if block[-2] == "\\" and block[-1] == "\n":
			block = block[:-2]

	return blocks

def block_to_blocktype(block):
	# Empty block handling
	if not block:
		return None

	# easy cases : no need for multiline checks
	if re.findall(r"^#{1,6}\ .*", block):
		return BlockType.HEADING
	elif re.findall(r"^```[\s\S]*?```$", block):
		return BlockType.CODE

	# multiline cases
	lines = block.split("\n")
	blocktype_checklist = []
	i = 1

	## creating a checklist
	for line in lines:
		line = line.lstrip()
		if re.match(r">", line):
			blocktype_checklist.append("quote")
			continue
		if re.match(r"-\s", line):
			blocktype_checklist.append("ulist")
			continue
		# Ordered Lists : First the re.match creates an object where our digit is contained. 
		# we then access it through the .group() method
		olist_match = re.match(r"(\d+)\.\s", line)
		if olist_match and int(olist_match.group(1)) == i:
			blocktype_checklist.append("olist")
			i+=1
			continue
		blocktype_checklist.append("paragraph")

	## checking the list
	if "paragraph" in blocktype_checklist:
		return BlockType.PARAGRAPH
	elif all(line_type == "quote" for line_type in blocktype_checklist):
		return BlockType.QUOTE
	elif all(line_type == "ulist" for line_type in blocktype_checklist):
		return BlockType.ULIST
	elif all(line_type == "olist" for line_type in blocktype_checklist):
		return BlockType.OLIST
	else:
		return BlockType.PARAGRAPH

# takes an HtmlNode and a blocktype and returns a stripped_value to be used to create an HtmlNode
# Doesn't handle Code, because Code has not inline treatment
# careful as this function assumes that the item values have <li></li>inside.
def strip_block_delimiter(htmlnode, blocktype):
	value = htmlnode.value
	stripped_values = []
	lines = value.split("\n")
	for line in lines:
		match blocktype:
			# the easy cases
			case BlockType.PARAGRAPH:
				stripped_values.append(line.lstrip())
			# It takes away the spaces on the left side, and removes the first character, which is either > or -
			case BlockType.QUOTE:
				stripped_values.append(line.lstrip()[1:].lstrip())

			# more difficult cases
			case BlockType.ULIST:
				print("==== ULIST, before strip : ", line)
				line = line.strip("<li>")
				line = line.strip("</li>")

				stripped = line.lstrip()[1:].lstrip()

				line = f"<li>{stripped}</li>"
				print("==== ULIST : ", line)

				stripped_values.append(line)

			case BlockType.OLIST:
				print("==== OLIST, before strip : ", line)
				line = line.strip("<li>")
				line = line.strip("</li>")

				olist_match = re.match(r"(\d+).*", line)
				# group 1 correspond to this part of the regex : (\d) which is the digit, then strip any remaining space
				stripped = line.strip(olist_match.group(1))
				stripped = stripped.strip(".").lstrip()

				line = f"<li>{stripped}</li>"
				print("===== OLIST : ", line)

				stripped_values.append(line)

			case BlockType.HEADING:
				heading_match = re.match(r"(#{1,6}).*", line)
				# same logic than OLIST
				stripped_values.append(line.strip(heading_match.group(1)).lstrip())
			case BlockType.CODE: # code needs no inline processing
				pass
			case _:
				raise Exception("blocktype must be a BlockType")
	stripped_value = "\n".join(stripped_values)

	return stripped_value


# text a single markdown inline text and returns htmlnodes.
# to be used to in the child_nodes argument 
# to create a ParentNode out of a single block text.
def text_to_htmlnodes(text):
	textnodes = text_to_textnode(text)
	htmlnodes = []
	for textnode in textnodes:
		htmlnodes.append(textnode_to_htmlnode(textnode))
	return htmlnodes

# Lists handler
def items_to_html(block, blocktype):
	items = block.split("\n")

	results = []
	for item in items:
		if blocktype == BlockType.ULIST or blocktype == BlockType.OLIST:
			string = f"<li>{item}</li>"
			results.append(string)
		else:
			return block

	result = "\n".join(results)
	return result


def markdown_to_html(text):
	if not text:
		return None

	blocks = markdown_to_blocks(text)

	for block in blocks:
		blocktype = block_to_blocktype(block) # figuring out the blocktype
		block = items_to_html(block, blocktype) # making sure the items have the right tag
		child_nodes = text_to_htmlnodes(block) # diving the block into htmlnodes
		child_values = []

		for child in child_nodes:
			child.value = strip_block_delimiter(child, blocktype)
		blocknodes = []
	
	return "Hello"



text = '''
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

1. This is 
2. An ordered list with *bold*

> Quote
> Life is a Miracle, God probably
'''
result = markdown_to_html(text)
print(result)