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
			results += f"{prop[0]}={prop[1]}"
		return results

	def __repr__(self):
		return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
