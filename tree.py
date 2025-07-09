from typing import Self


class Node:
    leaf: bool
    key: str
    value: float
    left: Self
    right: Self

    def __init__(self, leaf: bool = False, key: str = None, value: float = None, left: Self = None, right: Self = None):
        self.leaf = leaf
        if leaf:
            self.key = key
            self.value = value
        else:
            self.key = "in"
            self.value = left.value + right.value
            self.left = left
            self.right = right

    def __repr__(self):
        if self.leaf:
            return self.key + " : " + str(self.value)
        else:
            return (self.left.key + " : " + str(self.left.value) + " <- " + self.key + " : " + str(self.value)
                    + " -> " + self.right.key + " : " + str(self.right.value))

    def __lt__(self, other):
        return self.value < other.value
