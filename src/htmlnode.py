class HTMLNode():
	def __init__(self,tag=None,value=None,children=None,props=None):
		self.tag = tag
		self.value = value
		self.children = children
		self.props = props

	def __eq__(self,other):
			if not isinstance(other, HTMLNode):
				return False
			return (
				self.tag == other.tag and
				self.value == other.value and
				self.children == other.children and
				self.props == other.props
			)

	def to_html(self):
		raise NotImplementedError("Not implemented here")

	def props_to_html(self):
		results = ""
		if self.props:
			props = self.props.items()
		else:
			return results
		for prop in props:
			results += f' {prop[0]}="{prop[1]}"'
		return results

	def __repr__(self):
		return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

# a child class of HTMLNode but deals with "leafes" and not the "branches".
# i.e. it represents a single HTML tag with no children.
class LeafNode(HTMLNode):
	def __init__(self, tag, value, props=None):
		super().__init__(tag=tag,value=value,children=None,props=props)

	# Let's come back here another time. Test.sh to get the error. Possibly coming from here
	def to_html(self):
		if self.value == None:
			raise ValueError("All leaf nodes must have a value.")
		elif self.tag == None:
			return self.value
		else:
			return f"<{self.tag}{super().props_to_html()}>{self.value}</{self.tag}>"

## Our new ParentNode class will handle the nesting of HTML nodes inside of one another.
## Any HTML node that's not "leaf" node (i.e. it has children) is a "parent" node.
class ParentNode(HTMLNode):
	def __init__(self, tag, children, props=None):
		super().__init__(tag=tag,value=None,children=children,props=props)

	def to_html(self, child_list=None):
		if self.tag == None:
			raise ValueError("All parent nodes must have a value.")
		elif self.children == None:
			raise ValueError("All parent nodes must have children nodes.")
		elif child_list == None:
			child_list = self.children

		result = f"<{self.tag}{super().props_to_html()}>"

		if len(child_list) <= 1:
			result += child_list[0].to_html()
		else:
			for child in child_list:
				result += child.to_html() #TOCHANGE this was vibe coding without understanding...

		result += f"</{self.tag}>"
		return result


