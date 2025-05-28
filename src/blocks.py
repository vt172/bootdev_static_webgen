from enum import Enum
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
		line = line.strip()
		if re.findall(r"^>\s.*", line):
			blocktype_checklist.append("quote")
			continue
		if re.findall(r"^-\s.*", line):
			blocktype_checklist.append("ulist")
			continue
		olist_match = re.match(r"(\d)+\.\s", line)
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


print(block_to_blocktype("1. an item\n 32. an item\n 3. an item"))