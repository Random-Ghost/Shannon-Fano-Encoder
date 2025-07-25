from tree import Node


def to_char_dict(sentence: str) -> dict[str, float]:
    n: int = len(sentence)
    per: float = 1 / n
    char_dict: dict[str, float] = {}
    for char in sentence.lower():
        if char in char_dict.keys():
            char_dict[char] += per
        else:
            char_dict[char] = per
    return char_dict


def create_tree(node_list: list[Node], i: int, j: int) -> Node:
    # for the base case, if i = j we do not need to do any calculations as it will be a leaf node.
    if i == j:
        return node_list[i]

    temp_sum = 0
    for node in node_list[i:j + 1]:  # we have to make sure all items in the range are included.
        temp_sum += node.value
    threshold = temp_sum / 2

    # now we have the threshold, we have to find the split index.
    temp_sum = 0
    split_index = i
    for k in range(i, j):
        temp_sum += node_list[k].value
        split_index = k
        if temp_sum >= threshold:
            break

    # now we have the split index k
    return Node(left=create_tree(node_list, i, split_index), right=create_tree(node_list, split_index + 1, j))


class ShannonFano:
    root: Node

    def __init__(self, sentence: str = None, char_dict: dict[str, float] = None):
        self.encode_dict: dict[str, str] = {}  # mutable object

        if char_dict is None:
            char_dict: dict[str, float] = to_char_dict(sentence)

        # now we convert it to a node list.
        node_list: list[Node] = []
        for key, value in char_dict.items():
            node_list.append(Node(leaf=True, key=key, value=value))

        # the list has to be in descending order.
        node_list = sorted(node_list, reverse=True)

        n: int = len(node_list)
        self.root = create_tree(node_list, 0, n - 1)  # we have now created the tree structure.
        self.bin()  # we now have the code dictionary

    def bin(self) -> None:
        # we will use a BFS algorithm to find the code values of the characters.
        # 0 for left nodes and 1 for right nodes.
        temp_dict: dict[Node, str] = {self.root.left: "0", self.root.right: "1"}
        while len(temp_dict) >= 1:
            temp = next(iter(temp_dict))  # this gives us the first index on the dictionary
            # we should also note that temp is a Node object.
            # if it is a leaf node, we add it to encode_dict and remove it from temp_dict
            if temp.leaf:
                self.encode_dict[temp.key] = temp_dict[temp]
            else:
                temp_dict[temp.left] = temp_dict[temp] + "0"
                temp_dict[temp.right] = temp_dict[temp] + "1"
            temp_dict.pop(temp)

    def encode(self, sentence: str) -> str:
        code: str = ""
        for char in sentence.lower():
            code += self.encode_dict[char]
        return code

    def decode(self, code: str) -> str:
        sentence: str = ""
        pos = self.root
        for char in code:
            if char == "0":
                pos = pos.left
            else:  # I am not adding any try-catch functionalities. I will just hope it works.
                pos = pos.right
            # if we end on a leaf node, we add its key to the sentence and reset pos.
            if pos.leaf:
                sentence += pos.key
                pos = self.root
        return sentence
