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
def inject_htmltag_to_items(block,blocktype):
	items = block.split("\n")
	injected = []
	for item in items:
		item = item.lstrip()
		match blocktype:
			case BlockType.ULIST:
				tag = "ul"
				print("+++ ULIST line ", item)
				if item:
					stripped = item.strip("-").lstrip()

			case BlockType.OLIST:
				tag = "ol"
				olist_match = re.match(r"(\d+).*", item)
				# group 1 correspond to this part of the regex : (\d) which is the digit, then strip any remaining space
				if olist_match:
					stripped = item.strip(olist_match.group(1))
					stripped = stripped.strip(".").lstrip()

		tagged = f"<li>{stripped}</li>"
		injected.append(tagged)

	return "".join(injected)


# takes an HtmlNode and a blocktype and returns a stripped_value 
# AND tag to be used to create an HtmlNode
# Doesn't handle Code bloks, because Code has not inline treatment
def block_sanitizer(htmlnode, blocktype):
	value = htmlnode.value
	stripped_values = []
	stripped_items = []

	lines = value.split("\n")
	item_lines = value.split("<li>")

	for line in lines:
		match blocktype:
			case BlockType.PARAGRAPH:
				tag = "p"
				stripped_values.append(line)
			# It takes away the spaces on the left side, and removes the first character, which is either > or -
			case BlockType.QUOTE:
				tag = "blockquote"
				stripped_values.append(line.lstrip().strip(">").lstrip())
			# more difficult cases
			# careful here as it doesn't work for HEADINGS with multilines
			case BlockType.HEADING:
				heading_match = re.match(r"(#{1,6}).*", line)
				tag = f"h{len(heading_match.group(1))}"
				stripped = line.strip(heading_match.group(1)).lstrip()
				return stripped, tag
			case BlockType.CODE: # CODE, to come back here
				pass

			# ITEM CASES, see inject_htmltag_to_items for more info
			# Basically, those two were treated before.
			case BlockType.ULIST:
				stripped_values.append(line)
				tag = "ul"
			case BlockType.OLIST:
				stripped_values.append(line)
				tag = "ol"

	
	# Handle different joining strategies for different block types
	if blocktype == BlockType.PARAGRAPH:
	    stripped_value = " ".join(stripped_values)
	elif blocktype == BlockType.QUOTE:
	    stripped_value = "".join(stripped_values)  # No separator for quotes
	else:
	    stripped_value = "\n".join(stripped_values)

	# finally returning all values
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
		block = inject_htmltag_to_items(block, blocktype)
	child_nodes = text_to_htmlnodes(block) # diving the block into htmlnodes
	for child in child_nodes: # sanitizing data
		value, tag = block_sanitizer(child, blocktype)
		child.value = value
	return child_nodes, tag

def markdown_to_html(text):
	if not text:
		return None
	blocks = markdown_to_blocks(text)
	blocknodes = []

	for block in blocks:
		blocktype = block_to_blocktype(block)
		print(f"======\nBLOCKTYPE : {blocktype}")
		print("BLOCKNODE RESULTS :")
		if blocktype == BlockType.CODE:
			block = block[3:-3].lstrip()
			blocknode = LeafNode("pre",f"<code>{block}</code>")
		else:
			child_nodes, tag = prepare_block(block, blocktype)
			blocknode = ParentNode(tag, child_nodes)
		print(blocknode.to_html())

		blocknodes.append(blocknode) if blocknode else print("None")
	print("===== FINAL RESULTS:")
	print(ParentNode("div",blocknodes).to_html())

	return ParentNode("div",blocknodes)
