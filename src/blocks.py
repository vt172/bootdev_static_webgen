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

# takes a list block and returns an injected string
# with <li>
def inject_htmltag_to_items(block):
	items = block.split("\n")
	injected = []
	for item in items:
		tagged = f"<li>{item}</li>"
		injected.append(tagged)
	return "\n".join(injected)


# takes an HtmlNode and a blocktype and returns a stripped_value 
# AND tag to be used to create an HtmlNode
# Doesn't handle Code, because Code has not inline treatment
def block_sanitizer(htmlnode, blocktype):
	value = htmlnode.value
	stripped_values = []
	lines = value.split("\n")
	tag = ""
	for line in lines:
		match blocktype:
			# the easy cases
			case BlockType.PARAGRAPH:
				tag = "p"
				stripped_values.append(line.lstrip())
			# It takes away the spaces on the left side, and removes the first character, which is either > or -
			case BlockType.QUOTE:
				tag = "blockquote"
				stripped_values.append(line.lstrip().strip(">").lstrip())
			# more difficult cases
			case BlockType.ULIST:
				tag = "ul"
				stripped = line.strip("-").lstrip()
				stripped_values.append(stripped)

			case BlockType.OLIST:
				tag = "ol"
				olist_match = re.match(r"(\d+).*", line)
				# group 1 correspond to this part of the regex : (\d) which is the digit, then strip any remaining space
				if olist_match:
					stripped = line.strip(olist_match.group(1))
					stripped = stripped.strip(".").lstrip()
					stripped_values.append(stripped)

			# careful here as it doesn't work for HEADINGS with multilines
			case BlockType.HEADING:
				heading_match = re.match(r"(#{1,6}).*", line)
				tag = f"h{len(heading_match.group(1))}"
				stripped = line.strip(heading_match.group(1)).lstrip()
				return stripped, tag

			case BlockType.CODE: # code needs no inline processing
				pass
			case _:
				raise Exception("blocktype must be a BlockType")

	# finally returning all values
	stripped_value = "\n".join(stripped_values)
	return stripped_value, tag

# text a single markdown inline text and returns htmlnodes.
# to be used to in the child_nodes argument 
# to create a ParentNode out of a single block text.
def text_to_htmlnodes(text):
	textnodes = text_to_textnode(text)
	htmlnodes = []
	for textnode in textnodes:
		htmlnodes.append(textnode_to_htmlnode(textnode))
	return htmlnodes

# Prepare the block to be handled by create_blocknode
# it just calls the previous functions to sanitize
# the data for create_blocknode.
def prepare_block(block, blocktype):
	blocktype = block_to_blocktype(block) # figuring out the blocktype
	if blocktype == BlockType.ULIST or blocktype == BlockType.OLIST:
		block = inject_htmltag_to_items(block)
	child_nodes = text_to_htmlnodes(block) # diving the block into htmlnodes
	for child in child_nodes: # sanitizing data
		value, tag = block_sanitizer(child, blocktype)
		child.value = value
	return child_nodes, tag

# creates the ParentNode for the block : a "blocknode"
def create_blocknode(child_nodes,blocktype,tag):
	normal_cases = blocktype == BlockType.PARAGRAPH \
	or blocktype == BlockType.HEADING \
	or blocktype == BlockType.QUOTE \
	or blocktype == BlockType.ULIST \
	or blocktype == BlockType.OLIST

	if normal_cases:
		return ParentNode(tag,child_nodes)
	


def markdown_to_html(text):
	if not text:
		return None
	blocks = markdown_to_blocks(text)
	blocknodes = []
	for block in blocks:
		blocktype = block_to_blocktype(block)
		child_nodes, tag = prepare_block(block, blocktype)
		blocknode = create_blocknode(child_nodes, blocktype, tag)
		print("======\nBLOCKNODE RESULTS :")
		print(f"BLOCKTYPE : {blocktype}")
		print(blocknode.to_html())

		blocknodes.append(blocknode) if blocknode else print("None")
	
	return ParentNode("div",blocknodes)



text = '''
# the effect of Jesus on your body

This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

1. This is 
2. An ordered list with bold, **but with bold**

> Quote
> Life is a Miracle, **God** probably

- List
- List with _italic_
'''
result = markdown_to_html(text)
print("=====")
print("FINAL RESULTS: ",result)