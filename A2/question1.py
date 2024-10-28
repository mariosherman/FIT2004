class Node:
    def __init__(self):
        """
        Function description:
        Initialize a node with an array for children (one for each possible character 'A', 'B', 'C', 'D')
        and a list to store indexes where suffixes start.

        :Auxiliary Space Complexity:
        O(1)
        """
        self.children = [None] * 4  # Since the genome contains only 'A', 'B', 'C', 'D'
        self.indexes = []

class SuffixTrie:
    def __init__(self, text):
        """
        Function description:
        Initialize the root of the trie and build the suffix trie from the given text.

        :Input:
        text: A string representing the genome.

        :Output, return or postcondition:
        Initializes a SuffixTrie object with a built suffix trie.

        :Time Complexity:
        O(N^2)

        :Time Complexity Analysis:
        The function iterates over the text to insert all suffixes, and each insertion can take up to O(N) time.

        :Space Complexity:
        O(N^2)

        :Auxiliary Space Complexity:
        O(N^2)
        """
        self.root = Node()
        self.build_suffix_trie(text)

    def build_suffix_trie(self, text):
        """
        Function description:
        Insert all suffixes of the given text into the suffix trie.

        :Input:
        text: A string representing the genome.

        :Output, return or postcondition:
        The suffix trie is built from the 

        :Time Complexity:
        O(N^2)

        :Time Complexity Analysis:
        Each suffix insertion can take up to O(N) time, and there are N suffixes to insert.

        :Space Complexity:
        O(N^2)

        :Auxiliary Space Complexity:
        O(N^2)
        """
        n = len(text)
        for i in range(n):
            self.insert_suffix(text, i)

    def insert_suffix(self, text, start_index):
        """
        Function description:
        Insert a suffix starting at the given index into the trie.

        :Input:
        text: A string representing the genome.
        start_index: The starting index of the suffix to be inserted.

        :Output, return or postcondition:
        The suffix starting at start_index is inserted into the trie.

        :Time Complexity:
        O(N)

        :Time Complexity Analysis:
        Inserting a suffix involves traversing and potentially adding nodes for each character in the suffix.

        :Space Complexity:
        O(N)

        :Auxiliary Space Complexity:
        O(1)
        """
        current = self.root
        for i in range(start_index, len(text)):
            index = ord(text[i]) - ord('A')  # Convert character to index: 'A'-> 0, 'B'-> 1, etc.
            if not current.children[index]:
                current.children[index] = Node()  # Create a new node if necessary.

            current = current.children[index]
            current.indexes.append(start_index)  # Record the start index of this suffix.

    def search(self, pattern):
        """
        Function description:
        Search for all occurrences of the pattern in the suffix trie.

        :Input:
        pattern: A string pattern to search for in the trie.

        :Output, return or postcondition:
        A list of start indexes where the pattern is found in the text.

        :Time Complexity:
        O(T)

        :Time Complexity Analysis:
        Searching for a pattern involves traversing the trie for each character in the pattern, which takes linear time in the length of the pattern.

        :Space Complexity:
        O(1)

        :Auxiliary Space Complexity:
        O(1)
        """
        current = self.root
        for char in pattern:
            index = ord(char) - ord('A')  # Convert character to index.

            if not current.children[index]:
                return []  # Pattern not found
            current = current.children[index]

        return current.indexes  # Return all start indexes where the pattern is found.

    def __str__(self):
        """
        Function description:
        Provide a string representation of the suffix trie for debugging purposes.

        :Output, return or postcondition:
        A string representation of the trie.

        :Time Complexity:
        O(N^2)

        :Time Complexity Analysis:
        Building the string representation involves traversing the entire trie structure.

        :Space Complexity:
        O(N^2)

        :Auxiliary Space Complexity:
        O(N^2)
        """
        def build_str(node, depth):
            result = ""
            for i in range(4):
                if node.children[i] is not None:
                    result += " " * depth + chr(i + ord('A')) + " (" + ",".join(map(str, node.children[i].indexes)) + ")\n"
                    result += build_str(node.children[i], depth + 1)
            return result

        return build_str(self.root, 0)

class OrfFinder:
    def __init__(self, genome):
        """
        Function description:
        Initialize the OrfFinder object with the given genome and then build the suffix trie with it

        :Input:
        genome: A string representing the genome

        :Output, return or postcondition:
        Initializes an OrfFinder object with a suffix trie built from the genome.

        :Time Complexity:
        O(N^2)

        :Time Complexity Analysis:
        The constructor of the OrfFinder calls the suffix trie builder which takes O(N^2) time

        :Space Complexity:
        O(N^2)

        :Auxiliary Space Complexity:
        O(N^2)
        """
        self.genome = genome
        self.suffix_trie = SuffixTrie(genome)

    def find(self, start, end):
        """
        Description:
        Find all substrings in the genome that start with the given start sequence and end with the given end sequence

        :Input:
        start: A string representing the start pattern (prefix)
        end: A string representing the end pattern (suffix)

        :Output, return or postcondition:
        A list of substrings that start with start and end with end

        :Time Complexity:
        O(T + U + V)

        :Time Complexity Analysis:
        Searching for start and end takes O(T) and O(U) (respectively)
        Constructing the substrings takes O(V) where V = the total length of all found substrings

        :Space Complexity:
        O(V)

        :Auxiliary Space Complexity:
        O(V)
        """
        result = []
        start_positions = self.suffix_trie.search(start)  # Find all positions where 'start' occurs.
        end_positions = self.suffix_trie.search(end)  # Find all positions where 'end' occurs.

        for start_index in start_positions:
            for end_index in end_positions:
                if end_index >= start_index + len(start):  # Ensure 'end' occurs after 'start' without overlapping.
                    orf = self.genome[start_index:end_index + len(end)]
                    result.append(orf)  # Append the constructed string to the result list.

        return result

# Example usage:
if __name__ == "__main__":
    genome = "BCBCA"
    orf_finder = OrfFinder(genome)
    print(orf_finder.find("BC", "A"))  # Expected output: ['BCA']

    genome2 = "ABDAAABBABDBB"
    orf_finder = OrfFinder(genome2)
    print(orf_finder.find("ABD", "BB"))  # Expected output: ['ABDBB']

    print(orf_finder.suffix_trie)
