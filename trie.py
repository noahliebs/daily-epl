import unidecode

class TrieNode(object):
    """
    Our trie node implementation. Store a search word as a pointer to the full word
    """
    
    def __init__(self, char: str):
        self.char = char
        self.children = []
        # Is it the last character of the word.
        self.word_finished = False
        # Store the full names as a list
        self.value = []
    

    def add(self, raw_search_word: str, value: str):
        """
        Adding a word in the trie structure
        """
        search_word = self.normalize_search_string(raw_search_word)
        
        node = self
        for char in search_word:
            found_in_child = False
            # Search for the character in the children of the present `node`
            for child in node.children:
                if child.char == char:
                    # point the node to the child that contains this char
                    node = child
                    found_in_child = True
                    break
            # We did not find it so add a new chlid
            if not found_in_child:
                new_node = TrieNode(char)
                node.children.append(new_node)
                # And then point node to the new child
                node = new_node
        # Everything finished. Mark it as the end of a word and store the full value
        node.word_finished = True
        node.value.append(value)


    def find_prefix(self, raw_prefix: str):
        """
        Check and return 
          1. If the prefix exsists in any of the words we added so far
          2. If yes then return the set of all "full" words
        """
        prefix = self.normalize_search_string(raw_prefix)
        node = self
        # If the root node has no children, then return False.
        # Because it means we are trying to search in an empty trie
        if not node.children:
            return set()
        for char in prefix:
            char_not_found = True
            # Search through all the children of the present `node`
            for child in node.children:
                if child.char == char:
                    # We found the char existing in the child.
                    char_not_found = False
                    # Assign node as the child containing the char and break
                    node = child
                    break
            # Return empty set when we did not find a char.
            if char_not_found:
                return set()

        ## Now that we have the node, let's get all leaf nodes
        ## TO DO: If exact match, ignore partial matches --> Remove once dropdown is added
        if node.word_finished:
            for v in node.value:
                if self.normalize_search_string(v) == self.normalize_search_string(raw_prefix):
                    return set([v])
            return set(node.value)

        def dfs(nested_prefix, node):
            if node.word_finished:
                return node.value
            res = set()
            for child in node.children:
                res = res.union(dfs(nested_prefix + child.char, child))
            return res

        return dfs(prefix, node)
    
    def normalize_search_string(self, raw_string):
        return unidecode.unidecode(raw_string).lower() 