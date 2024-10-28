class Node:
    def __init__(self):
        # Initialize a node with an array for children (one for each possible character 'A', 'B', 'C', 'D')
        # and a list to store indexes where suffixes start.
        self.children = [None] * 4  # Since the genome contains only 'A', 'B', 'C', 'D'
        self.indexes = []

class SuffixTrie:
    def __init__(self, text):
        # Initialize the root of the trie and build the suffix trie from the given text.
        self.root = Node()
        self.build_suffix_trie(text)
        
    def build_suffix_trie(self, text):
        n = len(text)
        # Insert all suffixes of the text into the trie.
        for i in range(n):
            self.insert_suffix(text, i)
    
    def insert_suffix(self, text, start_index):
        current = self.root
        # Traverse and build the trie from the suffix starting at start_index.
        for i in range(start_index, len(text)):
            index = ord(text[i]) - ord('A')  # Convert character to index: 'A'-> 0, 'B'-> 1, etc.
            if not current.children[index]:
                current.children[index] = Node()  # Create a new node if necessary.
            current = current.children[index]
            current.indexes.append(start_index)  # Record the start index of this suffix.
    
    def search(self, pattern):
        current = self.root
        # Traverse the trie to find the pattern.
        for char in pattern:
            index = ord(char) - ord('A')  # Convert character to index.
            if not current.children[index]:
                return []  # If the pattern is not found, return an empty list.
            current = current.children[index]
        return current.indexes  # Return all start indexes where the pattern is found.
    

class OrfFinder:
    def __init__(self, genome):
        # Initialize the OrfFinder with the given genome and build the suffix trie.
        self.genome = genome
        self.n = len(genome)
        self.suffix_trie = SuffixTrie(genome)
    
    def find(self, start, end):
        result = []
        