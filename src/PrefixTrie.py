class TrieNode:
	def __init__(self):
		self.children = {}
		self.value = []

class PrefixTrie:
	def __init__(self):
		self.root = TrieNode()

	def insert(self, wordstack: list[str], value):
		node = self.root
		for word in wordstack:
			if word not in node.children:
				node.children[word] = TrieNode()
			node = node.children[word]
		node.value += [value]

	def search(self, path: list[str]):
		node = self.root
		for word in path:
			if word not in node.children:
				return []
			node = node.children[word]
		return node.value
