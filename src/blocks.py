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
	if re.findall(r"(^#{1,6}\ .+)|((^\s#{1,6}\ .+))", block):
		return BlockType.HEADING
	if re.findall(r"(^```[\s\S]*?```$)|(^\s```[\s\S]*?```$)", block):
		return BlockType.CODE
	if re.findall(r"(^(>.*\n?)+$)|(^\s(>.*\n?)+$)", block):
		return BlockType.QUOTE
	if re.findall(r"(^(-.*\n?)+$)|(^\s(-.*\n?)+$)", block):
		return BlockType.ULIST
	if re.findall(r"(\d. .+)|(\s\d. .+)", block):
		split_lines = block.split("\n")
		i = 1
		is_olist = True
		for line in split_lines:
			line = line.strip(' ')
			if int(line[0]) == i:
				i += 1
			else:
				is_olist = False
				break
		if is_olist:
			return BlockType.OLIST
		return BlockType.PARAGRAPH

	else:
		return BlockType.PARAGRAPH