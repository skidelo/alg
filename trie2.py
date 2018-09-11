class Node(object):
    def __init__(self, value=None):
        self.children = {}
        self.value = value

class Trie(object):
    def __init__(self):
        self.head = Node('')

    def is_prefix(self, prefix):
        cur_node = self.head
        for char in prefix:
            if char in cur_node.children:
                cur_node = cur_node.children.get(char)
            else:
                return False
        return True

    def find(self, word):
        cur_node = self.head
        for char in word:
            cur_node = cur_node.children.get(char)
            if not cur_node:
                return None
        return cur_node.value

    def insert(self, word):
        cur_node = self.head
        for char_i, char in enumerate(word):
            if char in cur_node.children:
                cur_node = cur_node.children.get(char)
            else:
                break

        for i in range(char_i, len(word)):
            next_node = Node()
            cur_node.children[word[i]] = next_node
            cur_node = next_node

        cur_node.value = word

if __name__ == '__main__':
    trie = Trie()
    print(trie.find('cat'))
    print(trie.find('dog'))
    trie.insert('cat')
    trie.insert('dog')
    print(trie.find('cat'))
    print(trie.find('dog'))
    print(trie.find('c'))
    print(trie.is_prefix('c'))
    print(trie.is_prefix('ca'))
    print(trie.is_prefix('cat'))
    print(trie.is_prefix('g'))
    print(trie.is_prefix('d'))
    print(trie.is_prefix('dogs'))

