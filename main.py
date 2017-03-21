class Node:
    def __init__(self, symbol=None, children=None, frequency=1, is_complete=False, depth=0):
        if children is None:
            self.children = {}
        else:
            self.children = children

        if symbol is not None:
            self.frequency = frequency
        else:
            self.frequency = 0

        self.is_complete = is_complete

        self.depth = depth

        if symbol is not None and len(symbol) > 1:
            self.add_word(symbol.lower.strip('\n'))
        else:
            self.symbol = symbol

    def add_word(self, word, index=0, depth=0, original_tree=None):
        """
        Adds a word to the tree

        :param str word: Word to add
        :param int index: Index of letter
        :param int depth: Depth in the tree
        :return: NoneType

        >>> tree = Node()
        >>> tree.add_word('hi')
        >>> tree.add_word('bye')
        >>> tree.add_word('what now')
        >>> tree
        {None: {'h': {'i': {}}, 'b': {'y': {'e'}}}}
        """
        if original_tree is None:
            original_tree = self

        if word[index] != '\n':
            # If not a new line

            if word[index] not in self.children:
                # If letter does not exist in the tree branch yet
                self.children[word[index]] = Node(word[index], depth=depth)
            else:
                # If the letter exists, increase it's frequency
                self.children[word[index]].frequency += 1

        if len(word) - 1 == index:
            # If last letter, means its a word
            self.children[word[index]].is_complete = True

        elif word[index + 1] == ' ':
            self.children[word[index]].is_complete = True
            original_tree.add_word(word[index + 2:])

        elif len(word) - 1 != index:
            # If end of the word has not been reached yet
            self.children[word[index].lower()].add_word(word, index=index+1, depth=depth + 1, original_tree=original_tree)

    def get_end(self, word, index=0):
        """
        Return the last leaf in the path, tree takes towards <word>

        :param str word: Word to find
        :param int index: Current index through word
        :return: Node

        >>> tree = Node()
        >>> tree.add_word('hello')
        >>> tree.get_end('hell') == tree.children['h'].children['e'].children['l'].children['l']
        True
        >>> tree.add_word('wow')
        >>> tree.get_end('wo') == tree.children['w'].children['o']
        True
        """

        if len(word) != index and word[index] != '\n':
                # If not a new line
                try:
                    return self.children[word[index]].get_end(word, index=index + 1)
                except KeyError:
                    return self

        # If next letter is not in the tree
        return self

    def is_word(self, word):
        """
        Return if word exists in tree

        :param str word: Word to find
        :return: bool

        >>> tree = Node()
        >>> tree.add_word('hello')
        >>> tree.add_word('hell')
        >>> tree.is_word('hell')
        True
        """

        return self.get_end(word).is_complete

    def _get_next_frequent(self, word, limit, top, degrade=0):
        """
        Keeps finding next, most-frequent leaf until limit is reached

        :param str word: Word to predict
        :param int limit: Limit of words to predict
        :param list of tuple of (str, int) top: List of words predicted
        :return: NoneType
        """

        # Rate next letters by frequency
        children = [(self.children[i], self.children[i].frequency) for i in self.children]
        children.sort(key=lambda x: x[1])

        for child in children:
            if len(top) == limit:
                # If limit is reached
                break
            elif child[0].is_complete and (word + child[0].symbol, child[0].frequency) not in top:
                # If a new word is found
                top.append((word + child[0].symbol, child[0].frequency))

            child[0]._get_next_frequent(word + child[0].symbol, limit, top)

    def find_most_frequent(self, word, limit=10):
        """
        Return the <limit> most likely words by frequency to the input

        :param str word: Word to get predictions for
        :param int limit: Limit of words to predict
        :return: NoneType | list of str

        >>> tree = Node()
        >>> tree.add_word('hello')
        >>> tree.add_word('howdy')
        >>> tree.add_word('hello friend')
        >>> tree.add_word('hows it going')
        >>> tree.find_most_frequent('ho')
        ['howdy', 'hows']
        """

        top = []

        while len(top) != limit and len(word) > 0:
            current_end_node = self.get_end(word)

            if not len(word) == 0 or len(word) == 1 and not len(current_end_node.children) == 0:

                # Get word so far
                word = word[:current_end_node.depth + 1]

                # Get words
                current_end_node._get_next_frequent(word, limit, top)

            if len(word) == 1:
                break
            else:
                word = word[:-1]

        if len(word) >= 1:
            return [val[0] for val in sorted(top, reverse=True, key=lambda x: x[1])]
        else:
            # If there's no word to predict
            return None

    def __repr__(self, cont=False):
        """

        :param output:
        :return:

        >>> tree = Node()
        >>> tree.add_word('hello')
        >>> tree.add_word('helt')
        >>> tree.add_word('what')
        >>> tree
        Node(None: Node(h: Node(e: Node(l: Node(l: Node(o: None)), Node(t: None)))), Node(w: Node(h: Node(a: Node(t: None)))))
        """
        output = 'Node(' + str(self.symbol) + ': '

        if len(self.children) == 0:
            output += 'None, '

        else:
            for child in self.children:
                output += str(self.children[child].__repr__()) + ', '

        return output[:-2] + ')'


if __name__ == "__main__":
    file = open('wordlist.txt', 'r')

    lines = file.readlines()

    tree = Node()

    for line in lines:
        tree.add_word(line.lower().strip('\n'))

    print(tree.find_most_frequent('he'))
