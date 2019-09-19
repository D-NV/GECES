import dill


class Test:
    def __init__(self, a=None):
        self.a = a


class Node:
    def __init__(self, left=None, right=None, data=""):
        self.left = left
        self.right = right
        self.data = data


node1 = Node()
node1.data = "+"
node1.left = Node()
node1.left.data = "a"
node1.right = Node()
node1.right.data = "b"

test1 = Test(node1)
# test2 = Test(30, 40)

with open("test.pkl", "wb") as out:
    dill.dump(test1, out)
    # dill.dump(test2, out)
#
# print(test1)

# with open("test.pkl", "rb") as input:
#     # test2 = dill.load(input)
#     test1 = dill.load(input)
#
# print(test1, "\t", test1.a, "\t", test1.a.data, "\t", test1.a.left, "\t", test1.a.left.data, "\t", test1.a.right, "\t", test1.a.right.data)
# print(test2, "\t", test2.a, "\t", test2.b)
