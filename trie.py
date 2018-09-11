class Node(object):
    def __init__(self):
        self._val = ''
        self._children = []
        self.parent = None
        self._is_word = False

    @property
    def is_word(self):
        return self._is_word

    @is_word.setter
    def is_word(self, value):
        self._is_word = value

    def contains(self, word):
        if not word.startswith(self.val):
            return None
        if self.val == word:
            return self

        result = None
        for child in self.children:
            result = child.contains(word)
            if result:
                break

        return result

    def add_child(self, word):
        child = Node()
        child._val = word
        self.children.append(child)
        child.parent = self
        return child

    @property
    def children(self):
        return self._children

    @property
    def val(self):
        return self._val


class Trie(object):
    def __init__(self):
        self._head = Node()

    def add_word(self, word):
        cur_node = self._head
        i = 0
        while i <= len(word):
            if cur_node.val == word[:i]:
                if i == len(word):
                    cur_node.is_word = True
                    break
                i += 1
                for child in cur_node.children:
                    if child.val == word[:i]:
                        cur_node = child
                        break
            else:
                cur_node = cur_node.add_child(word[:i])

    # Assumes a word can be a prefix of itself. 'dog' is prefix of 'dog'
    def get_prefix(self, prefix):
        return self._head.contains(prefix)

    def is_prefix(self, prefix):
        return True if self._head.contains(prefix) else False

    def is_word(self, word):
        node = self.get_prefix(word)
        return node and node.is_word


if __name__ == '__main__':
    trie = Trie()
    print(trie.is_word('cat'))
    print(trie.is_word('dog'))
    trie.add_word('cat')
    trie.add_word('dog')
    print(trie.is_word('cat'))
    print(trie.is_word('dog'))
    print(trie.is_word('d'))
    print(trie.is_prefix('d'))
    print(trie.is_prefix('do'))
    print(trie.is_prefix('dog'))
    print(trie.is_prefix('c'))
    print(trie.is_word('c'))
