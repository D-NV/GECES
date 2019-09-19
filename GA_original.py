import numpy as np
import pandas as pd
import random
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
import dill


class Node(object):
    def __init__(self, left=None, right=None, parent=None, data=""):
        self.left = left
        self.right = right
        self.parent = parent
        self.data = data

    def __str__(self):
        return str(self.data)


class Tree:
    def __init__(self, root=None, fitness=None, nodes=[], expression=None):
        self.root = root
        self.fitness = fitness
        self.nodes = nodes
        self.expression = expression


class Individual:
    def __init__(self, trees=[], fitness=None):
        self.trees = trees
        self.cumulativefitness = fitness


class Junction:
    left = Node()
    right = Node()
    left_cost = ''
    right_cost = ''
    data = ''


def makeTree(tree, root, maxlevel, features):
    function_set = ["+", "-", "*", "/"]
    try:
        tree.root = root
        tree.nodes = []
        tree.nodes.append(root)
        root.data = "P"+random.choice(function_set)
        root.parent = None
        generateTree(tree, root, 1, maxlevel, features)
    except Exception as e:
        print('Error in makeTree() function: \n', e)


def generateTree(tree, root, level, maxlevel, features):
    function_set = ["+", "-", "*", "/"]

    if level < maxlevel:
        if root.data.startswith("P"):
            if root.left is None:
                root.left = Node()
                root.left.data = "W"
                root.left.parent = root
                tree.nodes.append(root.left)
                generateTree(tree, root.left, level + 1, maxlevel, features)
            if root.right is None:
                root.right = Node()
                root.right.data = "W"
                root.right.parent = root
                tree.nodes.append(root.right)
                generateTree(tree, root.right, level + 1, maxlevel, features)
        elif root.data == "W":
            r = random.uniform(0, 1)

            if r < 0.7869:
                temp_random = random.uniform(0, 1)
                if root.left is None:
                    root.left = Node()
                    if temp_random < 0.7:
                        root.left.data = random.choice(function_set)
                    else:
                        root.left.data = str(random.uniform(0, 1))
                    root.left.parent = root
                    tree.nodes.append(root.left)

                    generateTree(tree, root.left, level + 1, maxlevel, features)
                if root.right is None:
                    root.right = Node()
                    if temp_random < 0.6:
                        root.right.data = "P"+random.choice(function_set)
                    else:
                        root.right.data = random.choice(features)
                    root.right.parent = root
                    tree.nodes.append(root.right)
                    generateTree(tree, root.right, level + 1, maxlevel, features)
            elif r > 0.7869:
                temp_random = random.uniform(0, 1)
                if root.left is None:
                    root.left = Node()
                    root.left.data = random.choice(function_set)
                    root.left.parent = root
                    tree.nodes.append(root.left)
                    generateTree(tree, root.left, level + 1, maxlevel, features)
                if root.right is None:
                    root.right = Node()
                    if temp_random < 0.35:
                        root.right.data = "P"+random.choice(function_set)
                    else:
                        root.right.data = random.choice(features)
                    root.right.parent = root
                    tree.nodes.append(root.right)
                    generateTree(tree, root.right, level + 1, maxlevel, features)
        elif root.data in (function_set[:-1] + function_set[0:]):
            if root.left is None:
                root.left = Node()
                root.left.data = str(random.uniform(0, 1))
                root.left.parent = root
                tree.nodes.append(root.left)
                generateTree(tree, root.left, level + 1, maxlevel, features)
            if root.right is None:
                root.right = Node()
                root.right.data = str(random.uniform(0, 1))
                root.right.parent = root
                tree.nodes.append(root.right)
                generateTree(tree, root.right, level + 1, maxlevel, features)
    else:
        if root.data == "W":
            if root.left is None:
                root.left = Node()
                root.left.data = str(random.uniform(0, 1))
                root.left.parent = root
                tree.nodes.append(root.left)
            if root.right is None:
                root.right = Node()
                root.right.data = random.choice(features)
                root.right.parent = root
                tree.nodes.append(root.right)


def printTree(root):
    current_level = [root]
    while current_level:
        print(' '.join(str(node.data) for node in current_level))
        next_level = list()
        for n in current_level:
            if n.left is not None:
                next_level.append(n.left)
            if n.right is not None:
                next_level.append(n.right)
            current_level = next_level


def postOrder(root):
    expr_post = []
    if root is not None:
        postOrder(root.left)
        postOrder(root.right)
        expr_post.append(root.data)
    return expr_post


def inOrder(root):
    expr_in = ""
    if root is not None:
        expr_in = root.left.data + root.data + root.right.data
    return expr_in


def updateNodes(curTree, curNode):
    if curTree.root not in curTree.nodes:
        curTree.nodes.append(curTree.root)
    if curNode.left is not None:
        curTree.nodes.append(curNode.left)
        updateNodes(curTree, curNode.left)
    if curNode.right is not None:
        curTree.nodes.append(curNode.right)
        updateNodes(curTree, curNode.right)


def CloneTree(curNode):
    if curNode is None:
        return None
    y = Node()
    y.data = curNode.data
    y.parent = None
    y.left = CloneTree(curNode.left)
    y.right = CloneTree(curNode.right)
    if y.left is not None:
        y.left.parent = y
    if y.right is not None:
        y.right.parent = y
    return y


def swapSubTrees(a, b):
    if a.parent is None or b.parent is None:
        return None
    parent1 = a.parent
    parent2 = b.parent

    if parent1.left is a and parent2.left is b:
        parent1.left = b
        parent2.left = a
    if parent1.left is a and parent2.right is b:
        parent1.left = b
        parent2.right = a
    if parent1.right is a and parent2.left is b:
        parent1.right = b
        parent2.left = a
    if parent1.right is a and parent2.right is b:
        parent1.right = b
        parent2.right = a


def activationFunction(weightedSum):
    # if weightedSum < 0:
    #     return str(1 - 1 / (1 + math.exp(weightedSum)))
    # return str(1 / (1 + math.exp(-weightedSum)))
    return str(weightedSum)


# def generateExpression(root, list):
#     if root is not None:
#         generateExpression(root.left, list)
#         list.append(root)
#         generateExpression(root.right, list)
#     return list


# def gptoanntree(root):
#     simplifyTree(root)
#     convertTree(root)
#     # new_root = Junction()
#     # new_root.data = "P"
#     # annTree(root, new_root)
#     # return new_root
#
#
# def simplifyTree(curNode):
#     function_set = ["+", "-", "*", "/"]
#     if curNode is not None:
#         simplifyTree(curNode.left)
#         if curNode.data in function_set:
#             if curNode.data == "+":
#                 curNode.data = str(float(curNode.left.data)+float(curNode.right.data))
#                 curNode.left = None
#                 curNode.right = None
#             elif curNode.data == "-":
#                 curNode.data = str(float(curNode.left.data)-float(curNode.right.data))
#                 curNode.left = None
#                 curNode.right = None
#             elif curNode.data == "*":
#                 curNode.data = str(float(curNode.left.data)*float(curNode.right.data))
#                 curNode.left = None
#                 curNode.right = None
#             elif curNode.data == "/":
#                 curNode.data = str(float(curNode.left.data)/float(curNode.right.data))
#                 curNode.left = None
#                 curNode.right = None
#         simplifyTree(curNode.right)
#
#
# def convertTree(curNode):
#     if curNode is not None:
#         convertTree(curNode.left)
#         if curNode.data == "W":
#             curNode.data = curNode.left.data
#             curNode.left = None
#         convertTree(curNode.right)
#
#
# def annTree(curNode, curJunc):
#     if curNode is not None:
#         annTree(curNode.left, curJunc)
#         if curNode.data == "P":
#             if curJunc.left is None and curJunc.right is None:
#                 curJunc.left_cost = curNode.left.data
#                 curJunc.right_cost = curNode.right.data
#                 curJunc.left = Junction()
#                 curJunc.right = Junction()
#                 curJunc.left.data = curNode.left.right.data
#                 curJunc.right.data = curNode.right.right.data
#             else:
#                 annTree(curNode, curJunc.left)
#
#                 annTree(curNode, curJunc.right)
#         annTree(curNode.right, curJunc)


def forceStop(event, trainingAcc):
    trainingAcc = 0
    print("Stopping the training process...")
    return trainingAcc


def evalTree(tree, root, dataSet):
    a = tree
    temproot = root
    a.root = temproot
    a.nodes = tree.nodes
    evalTreeStep1(a, temproot, dataSet)
    evalTreeStep2(a, temproot)


# def evaluateTree(tree, curNode, dataSet):
#     function_set = ["+", "-", "*", "/"]
#     if curNode is not None:
#         evaluateTree(tree, curNode.left, dataSet)
#         if curNode.data
#         evaluateTree(tree, curNode.right, dataSet)


def evalTreeStep1(tree, curNode, dataSet):
    function_set = ["+", "-", "*", "/"]
    if curNode is not None:
        evalTreeStep1(tree, curNode.left, dataSet)
        if curNode.data in function_set:
            if curNode.left is not None and curNode.right is not None:
                if curNode.data == "+":
                    curNode.data = str(float(curNode.left.data) + float(curNode.right.data))
                    curNode.left = None
                    curNode.right = None
                elif curNode.data == "-":
                    curNode.data = str(float(curNode.left.data) - float(curNode.right.data))
                    curNode.left = None
                    curNode.right = None
                elif curNode.data == "*":
                    curNode.data = str(float(curNode.left.data) * float(curNode.right.data))
                    curNode.left = None
                    curNode.right = None
                elif curNode.data == "/":
                    if float(curNode.right.data) == 0:
                        curNode.right.data = str(1)
                    curNode.data = str(float(curNode.left.data) / float(curNode.right.data))
                    curNode.left = None
                    curNode.right = None
        elif curNode.data.startswith("f"):
            curNode.data = str(dataSet[int(curNode.data[-1])])
        evalTreeStep1(tree, curNode.right, dataSet)


def evalTreeStep2(tree, curNode):
    if curNode is not None:
        if curNode.data == "W":
            evalTreeStep2(tree, curNode.left)
            evalTreeStep2(tree, curNode.right)
            curNode.data = str(float(curNode.left.data)*float(curNode.right.data))
            curNode.left = None
            curNode.right = None
        elif curNode.data.startswith("P"):
            if curNode.data[-1] == "+":
                evalTreeStep2(tree, curNode.left)
                evalTreeStep2(tree, curNode.right)
                curNode.data = str(float(curNode.left.data) + float(curNode.right.data))
                curNode.left = None
                curNode.right = None
            elif curNode.data[-1] == "-":
                evalTreeStep2(tree, curNode.left)
                evalTreeStep2(tree, curNode.right)
                curNode.data = str(float(curNode.left.data) - float(curNode.right.data))
                curNode.left = None
                curNode.right = None
            elif curNode.data[-1] == "*":
                evalTreeStep2(tree, curNode.left)
                evalTreeStep2(tree, curNode.right)
                curNode.data = str(float(curNode.left.data) * float(curNode.right.data))
                curNode.left = None
                curNode.right = None
            else:
                evalTreeStep2(tree, curNode.left)
                evalTreeStep2(tree, curNode.right)
                if float(curNode.right.data) == 0:
                    curNode.right.data = str(1)
                curNode.data = str(float(curNode.left.data) / float(curNode.right.data))
                curNode.left = None
                curNode.right = None

    # function_set = ["+", "-", "*", "/"]
    # rand = random.choice(function_set)
    # if curNode is not None:
    #     if curNode.data[-1] == "+":
    #         if curNode.left.data.startswith("W"):
    #             evalTreeStep2(tree, curNode.left)
    #             if curNode.right.data.startswith("W"):
    #                 weightedSum = float(curNode.left.data[1:]) * float(curNode.left.right.data) + float(
    #                     curNode.right.data[1:])
    #                 curNode.data = activationFunction(weightedSum)
    #                 curNode.left = None
    #                 curNode.right = None
    #             else:
    #                 print(curNode.left.right.data)
    #                 weightedSum = float(curNode.left.data[1:]) * float(curNode.left.right.data) + float(curNode.right.data)
    #                 curNode.data = activationFunction(weightedSum)
    #                 curNode.left = None
    #                 curNode.right = None
    #         elif curNode.right.data.startswith("W"):
    #             evalTreeStep2(tree, curNode.right)
    #             if curNode.left.data.startswith("W"):
    #                 weightedSum = float(curNode.right.data[1:]) * float(curNode.right.right.data) + float(
    #                     curNode.left.data[1:])
    #                 curNode.data = activationFunction(weightedSum)
    #                 curNode.left = None
    #                 curNode.right = None
    #             else:
    #                 weightedSum = float(curNode.right.data[1:]) * float(curNode.right.right.data) + float(
    #                     curNode.left.data)
    #                 curNode.data = activationFunction(weightedSum)
    #                 curNode.left = None
    #                 curNode.right = None
    #         else:
    #             weightedSum = float(curNode.left.data) + float(curNode.right.data)
    #             curNode.data = activationFunction(weightedSum)
    #             curNode.left = None
    #             curNode.right = None
    #     elif curNode.data[-1] == "-":
    #         if curNode.left.data.startswith("W"):
    #             evalTreeStep2(tree, curNode.left)
    #             if curNode.right.data.startswith("W"):
    #                 weightedSum = float(curNode.left.data[1:]) * float(curNode.left.right.data) - float(
    #                     curNode.right.data[1:])
    #                 curNode.data = activationFunction(weightedSum)
    #                 curNode.left = None
    #                 curNode.right = None
    #             else:
    #                 weightedSum = float(curNode.left.data[1:]) * float(curNode.left.right.data) - float(curNode.right.data)
    #                 curNode.data = activationFunction(weightedSum)
    #                 curNode.left = None
    #                 curNode.right = None
    #         elif curNode.right.data.startswith("W"):
    #             evalTreeStep2(tree, curNode.right)
    #             if curNode.left.data.startswith("W"):
    #                 weightedSum = float(curNode.right.data[1:]) * float(curNode.right.right.data) - float(
    #                     curNode.left.data[1:])
    #                 curNode.data = activationFunction(weightedSum)
    #                 curNode.left = None
    #                 curNode.right = None
    #             else:
    #                 weightedSum = float(curNode.right.data[1:]) * float(curNode.right.right.data) - float(
    #                     curNode.left.data)
    #                 curNode.data = activationFunction(weightedSum)
    #                 curNode.left = None
    #                 curNode.right = None
    #         else:
    #             weightedSum = float(curNode.left.data) - float(curNode.right.data)
    #             curNode.data = activationFunction(weightedSum)
    #             curNode.left = None
    #             curNode.right = None
    #     elif curNode.data[-1] == "*":
    #         if curNode.left.data.startswith("W"):
    #             evalTreeStep2(tree, curNode.left)
    #             if curNode.right.data.startswith("W"):
    #                 weightedSum = float(curNode.left.data[1:]) * float(curNode.left.right.data) * float(
    #                     curNode.right.data[1:])
    #                 curNode.data = activationFunction(weightedSum)
    #                 curNode.left = None
    #                 curNode.right = None
    #             else:
    #                 weightedSum = float(curNode.left.data[1:]) * float(curNode.left.right.data) * float(curNode.right.data)
    #                 curNode.data = activationFunction(weightedSum)
    #                 curNode.left = None
    #                 curNode.right = None
    #         elif curNode.right.data.startswith("W"):
    #             evalTreeStep2(tree, curNode.right)
    #             if curNode.left.data.startswith("W"):
    #                 weightedSum = float(curNode.right.data[1:]) * float(curNode.right.right.data) * float(
    #                     curNode.left.data[1:])
    #                 curNode.data = activationFunction(weightedSum)
    #                 curNode.left = None
    #                 curNode.right = None
    #             else:
    #                 weightedSum = float(curNode.right.data[1:]) * float(curNode.right.right.data) * float(
    #                     curNode.left.data)
    #                 curNode.data = activationFunction(weightedSum)
    #                 curNode.left = None
    #                 curNode.right = None
    #         else:
    #             weightedSum = float(curNode.left.data) * float(curNode.right.data)
    #             curNode.data = activationFunction(weightedSum)
    #             curNode.left = None
    #             curNode.right = None
    #     elif curNode.data[-1] == "/":
    #         if curNode.left.data.startswith("W"):
    #             evalTreeStep2(tree, curNode.left)
    #             if curNode.right.data.startswith("W"):
    #                 if float(curNode.right.data[1:]) == 0:
    #                     curNode.right.data[1:] = str(1)
    #                 weightedSum = float(curNode.left.data[1:]) * float(curNode.left.right.data) / float(
    #                     curNode.right.data[1:])
    #                 curNode.data = activationFunction(weightedSum)
    #                 curNode.left = None
    #                 curNode.right = None
    #             else:
    #                 if float(curNode.right.data) == 0:
    #                     curNode.right.data = str(1)
    #                 weightedSum = float(curNode.left.data[1:]) * float(curNode.left.right.data) / float(curNode.right.data)
    #                 curNode.data = activationFunction(weightedSum)
    #                 curNode.left = None
    #                 curNode.right = None
    #         elif curNode.right.data.startswith("W"):
    #             evalTreeStep2(tree, curNode.right)
    #             if curNode.left.data.startswith("W"):
    #                 if float(curNode.left.data[1:]) == 0:
    #                     curNode.left.data[1:] = str(1)
    #                 weightedSum = float(curNode.right.data[1:]) * float(curNode.right.right.data) / float(
    #                     curNode.left.data[1:])
    #                 curNode.data = activationFunction(weightedSum)
    #                 curNode.left = None
    #                 curNode.right = None
    #             else:
    #                 if float(curNode.left.data) == 0:
    #                     curNode.left.data = str(1)
    #                 weightedSum = float(curNode.right.data[1:]) * float(curNode.right.right.data) / float(
    #                     curNode.left.data)
    #                 curNode.data = activationFunction(weightedSum)
    #                 curNode.left = None
    #                 curNode.right = None
    #         else:
    #             if float(curNode.right.data) == 0:
    #                 curNode.right.data = str(1)
    #             weightedSum = float(curNode.left.data) / float(curNode.right.data)
    #             curNode.data = activationFunction(weightedSum)
    #             curNode.left = None
    #             curNode.right = None
    #     elif curNode.data.startswith("W"):
    #         evalTreeStep2(tree, curNode.right)


def calcFitness(tree, sample, index):
    fitness = 0
    # sample = pd.DataFrame(sample)
    # samplesize = len(sample.loc[sample.iloc[:, -1] == index])
    # sample = np.array(sample)
    samplesize = len(sample)
    # print("s = ",samplesize)
    out = -1
    for i in sample:
        t = Tree()
        t.root = CloneTree(tree.root)
        evalTree(t, t.root, i)
        # print(t.root.data)
        # print(t.root.data)
        if float(t.root.data) > 0:
            if index == 0:
                out = 0
            elif index == 1:
                out = 1
            elif index == 2:
                out = 2
            elif index == 3:
                out = 3
            elif index == 4:
                out = 4
            elif index == 5:
                out = 5
            elif index == 6:
                out = 6
            elif index == 7:
                out = 7
            # print(out)
        if out == i[-1] or (out == -1 and i[-1] != index):
            fitness += 1
            # print(fitness)
        else:
            fitness += 0

    output = (fitness/samplesize)*100
    # print(output)
    tree.fitness = output
    return output


def crossover(t1, t2, sample, index):
    a = t1
    b = t2
    new_a = Tree()
    new_b = Tree()
    new_a.root = CloneTree(a.root)
    new_b.root = CloneTree(b.root)
    updateNodes(new_a, new_a.root)
    updateNodes(new_b, new_b.root)
    nodes_a = new_a.nodes.copy()
    nodes_b = new_b.nodes.copy()
    pnodes_a = []
    pnodes_b = []
    wnodes_a = []
    wnodes_b = []
    # print(nodes_a)

    for i in nodes_a:
        if i.data.startswith("P"):
            pnodes_a.append(i)
            # print(i)
        elif i.data == "W":
            wnodes_a.append(i)
    for i in nodes_b:
        if i.data.startswith("P"):
            pnodes_b.append(i)
        elif i.data == "W":
            wnodes_b.append(i)

    # print(pnodes_a)
    if new_a.root in pnodes_a:
        pnodes_a.remove(new_a.root)
    if new_b.root in pnodes_b:
        pnodes_b.remove(new_b.root)

    parent1, parent2 = None, None

    randomNum = random.uniform(0, 10)
    if len(pnodes_a) == 0 or len(pnodes_b) == 0:
        parent1 = random.choice(wnodes_a)
        parent2 = random.choice(wnodes_b)
    else:
        if randomNum < 2.2265:
            parent1 = random.choice(pnodes_a)
            parent2 = random.choice(pnodes_b)
        elif 2.2265 < randomNum < 8.7635:
            parent1 = random.choice(wnodes_a)
            parent2 = random.choice(wnodes_b)
        else:
            parent1 = random.choice(pnodes_a)
            parent2 = random.choice(pnodes_b)

    cycle = 0
    while 1:
        if cycle < 30:
            # print(cycle)
            swapSubTrees(parent1, parent2)
            # print("a ", a, printTree(a.root))
            # print("b ", b, printTree(b.root))
            # print("new_a ", new_a, printTree(new_a.root))
            # print("new_b ", new_b, printTree(new_b.root))
            new_a.nodes.clear()
            updateNodes(new_a, new_a.root)
            new_b.nodes.clear()
            updateNodes(new_b, new_b.root)
            fit_a = a.fitness
            # print("fit_a = ", fit_a)
            fit_b = b.fitness
            # print("fit_b = ", fit_b)
            fit_new_a = calcFitness(new_a, sample, index)
            # print("fit_new_a = ", fit_new_a)
            fit_new_b = calcFitness(new_b, sample, index)
            rem_trees_b = []
            rem_trees_a = []
            # print("fit_new_b = ", fit_new_b)

            if (fit_new_a > fit_a and fit_new_a > fit_b) or (fit_new_b > fit_a and fit_new_b > fit_b):
                break
            # elif (fit_new_a > fit_a and fit_new_a > fit_b) and not (fit_new_b > fit_a and fit_new_b > fit_b):
            #     c = Tree()
            #     c.root = CloneTree(a.root)
            #     d = Tree()
            #     d.root = CloneTree(b.root)
            #     e = Tree()
            #     e.root = CloneTree(new_b.root)
            #     rem_trees_a.append(c)
            #     rem_trees_a.append(d)
            #     rem_trees_a.append(e)
            #     test = 0
            #     temp = None
            #     for i in rem_trees_a:
            #         if calcFitness(i, sample, index) > test:
            #             temp = i
            #     new_b.root = CloneTree(temp.root)
            #     updateNodes(new_b, new_b.root)
            #     pnodes_b.clear()
            #     wnodes_b.clear()
            #     nodes_b = new_b.nodes.copy()
            #
            #     for i in nodes_b:
            #         if i.data.startswith("P"):
            #             pnodes_b.append(i)
            #         elif i.data == "W":
            #             wnodes_b.append(i)
            #
            #     if new_b.root in pnodes_b:
            #         pnodes_b.remove(new_b.root)
            #
            #     randomNum = random.uniform(0, 10)
            #     if len(pnodes_a) == 0 or len(pnodes_b) == 0:
            #         parent1 = random.choice(wnodes_a)
            #         parent2 = random.choice(wnodes_b)
            #     else:
            #         if randomNum < 2.2265:
            #             parent1 = random.choice(pnodes_a)
            #             parent2 = random.choice(pnodes_b)
            #         elif 2.2265 < randomNum < 8.7635:
            #             parent1 = random.choice(wnodes_a)
            #             parent2 = random.choice(wnodes_b)
            #         else:
            #             parent1 = random.choice(pnodes_a)
            #             parent2 = random.choice(pnodes_b)
            # elif not (fit_new_a > fit_a and fit_new_a > fit_b) and (fit_new_b > fit_a and fit_new_b > fit_b):
            #     c = Tree()
            #     c.root = CloneTree(a.root)
            #     d = Tree()
            #     d.root = CloneTree(b.root)
            #     e = Tree()
            #     e.root = CloneTree(new_a.root)
            #     rem_trees_b.append(c)
            #     rem_trees_b.append(d)
            #     rem_trees_b.append(e)
            #     test = 0
            #     temp = None
            #     for i in rem_trees_b:
            #         if calcFitness(i, sample, index) > test:
            #             temp = i
            #     new_a.root = CloneTree(temp.root)
            #     updateNodes(new_a, new_a.root)
            #     pnodes_a.clear()
            #     wnodes_a.clear()
            #     nodes_a = new_a.nodes.copy()
            #
            #     for i in nodes_a:
            #         if i.data.startswith("P"):
            #             pnodes_a.append(i)
            #         elif i.data == "W":
            #             wnodes_a.append(i)
            #
            #     if new_a.root in pnodes_a:
            #         pnodes_a.remove(new_a.root)
            #
            #     randomNum = random.uniform(0, 10)
            #     if len(pnodes_a) == 0 or len(pnodes_b) == 0:
            #         parent1 = random.choice(wnodes_a)
            #         parent2 = random.choice(wnodes_b)
            #     else:
            #         if randomNum < 2.2265:
            #             parent1 = random.choice(pnodes_a)
            #             parent2 = random.choice(pnodes_b)
            #         elif 2.2265 < randomNum < 8.7635:
            #             parent1 = random.choice(wnodes_a)
            #             parent2 = random.choice(wnodes_b)
            #         else:
            #             parent1 = random.choice(pnodes_a)
            #             parent2 = random.choice(pnodes_b)
            else:
                new_a = Tree()
                new_b = Tree()
                new_a.root = CloneTree(a.root)
                new_b.root = CloneTree(b.root)
                updateNodes(new_a, new_a.root)
                updateNodes(new_b, new_b.root)
                pnodes_a.clear()
                pnodes_b.clear()
                wnodes_a.clear()
                wnodes_b.clear()
                nodes_a = new_a.nodes.copy()
                nodes_b = new_b.nodes.copy()

                for i in nodes_a:
                    if i.data.startswith("P"):
                        pnodes_a.append(i)
                    elif i.data == "W":
                        wnodes_a.append(i)
                for i in nodes_b:
                    if i.data.startswith("P"):
                        pnodes_b.append(i)
                    elif i.data == "W":
                        wnodes_b.append(i)

                if new_a.root in pnodes_a:
                    pnodes_a.remove(new_a.root)
                if new_b.root in pnodes_b:
                    pnodes_b.remove(new_b.root)

                randomNum = random.uniform(0, 10)
                if len(pnodes_a) == 0 or len(pnodes_b) == 0:
                    parent1 = random.choice(wnodes_a)
                    parent2 = random.choice(wnodes_b)
                else:
                    if randomNum < 2.2265:
                        parent1 = random.choice(pnodes_a)
                        parent2 = random.choice(pnodes_b)
                    elif 2.2265 < randomNum < 8.7635:
                        parent1 = random.choice(wnodes_a)
                        parent2 = random.choice(wnodes_b)
                    else:
                        parent1 = random.choice(pnodes_a)
                        parent2 = random.choice(pnodes_b)
        else:
            new_a.root = CloneTree(t1.root)
            new_b.root = CloneTree(t2.root)
            updateNodes(new_a, new_a.root)
            updateNodes(new_b, new_b.root)
            calcFitness(new_a, sample, index)
            calcFitness(new_b, sample, index)
            break
        cycle += 1
    return new_a, new_b


def standardCrossover(t1, t2, index):
    # a = Tree()
    a = t1
    b = t2
    # b = Tree()
    # a.root = CloneTree(t1.root)
    # b.root = CloneTree(t2.root)
    # updateNodes(a, a.root)
    # updateNodes(b, b.root)
    new_a = Tree()
    new_b = Tree()
    new_a.root = CloneTree(a.root)
    new_b.root = CloneTree(b.root)
    # printTree(a.root)
    # printTree(b.root)
    # printTree(new_a.root)
    # printTree(new_b.root)
    # print(a.nodes)
    updateNodes(new_a, new_a.root)
    updateNodes(new_b, new_b.root)
    nodes_a = new_a.nodes.copy()
    # print(nodes_a)
    nodes_b = new_b.nodes.copy()
    # print(nodes_b)
    pnodes_a = []
    pnodes_b = []
    wnodes_a = []
    wnodes_b = []

    for i in nodes_a:
        if i.data.startswith("P"):
            pnodes_a.append(i)
        elif i.data == "W":
            wnodes_a.append(i)
    for i in nodes_b:
        if i.data.startswith("P"):
            pnodes_b.append(i)
        elif i.data == "W":
            wnodes_b.append(i)

    if new_a.root in pnodes_a:
        pnodes_a.remove(new_a.root)
    if new_b.root in pnodes_b:
        pnodes_b.remove(new_b.root)

    # print(pnodes_a)
    # print(pnodes_b)
    # print(wnodes_a)
    # print(wnodes_b)
    parent1, parent2 = None, None

    randomNum = random.uniform(0, 10)
    if len(pnodes_a) == 0 or len(pnodes_b) == 0:
        parent1 = random.choice(wnodes_a)
        parent2 = random.choice(wnodes_b)
    else:
        if randomNum < 2.2265:
            parent1 = random.choice(pnodes_a)
            parent2 = random.choice(pnodes_b)
        elif 2.2265 < randomNum < 8.7635:
            parent1 = random.choice(wnodes_a)
            parent2 = random.choice(wnodes_b)
        else:
            parent1 = random.choice(pnodes_a)
            parent2 = random.choice(pnodes_b)

    # print(parent1)
    # printTree(parent1)
    # print(parent2)
    # printTree(parent2)

    swapSubTrees(parent1, parent2)
    # printTree(new_a.root)
    # printTree(new_b.root)
    new_a.nodes.clear()
    updateNodes(new_a, new_a.root)
    new_b.nodes.clear()
    updateNodes(new_b, new_b.root)

    return new_a, new_b


def mutation(a, sample, index):
    function_set = ["+", "-", "*", "/"]
    feature_set = ["f0", "f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9"]
    new_a = Tree()
    new_a.root = CloneTree(a.root)
    new_a.nodes = []
    updateNodes(new_a, new_a.root)
    nodes = new_a.nodes
    funcnodes = []
    doublenodes = []
    pnodes = []
    mutationnode = None

    for i in nodes:
        if i.data in function_set:
            funcnodes.append(i)
        elif i.data not in function_set and not i.data.startswith("P") and i.data != "W" and i.data not in feature_set:
            # print(i.data)
            doublenodes.append(i)
        elif i.data.startswith("P"):
            pnodes.append(i)

    randomNum = random.uniform(0, 10)
    if len(funcnodes) == 0:
        if randomNum < 7.283:
            mutationnode = random.choice(pnodes)
        else:
            mutationnode = random.choice(doublenodes)
    else:
        if randomNum < 3.2839:
            mutationnode = random.choice(funcnodes)
        elif 3.2839 < randomNum < 8.468:
            mutationnode = random.choice(pnodes)
        else:
            mutationnode = random.choice(doublenodes)

    cycle = 0

    while 1:
        if cycle < 30:
            if mutationnode.data in function_set:
                mutationnode.data = random.choice(function_set)
            elif mutationnode.data.startswith("P"):
                mutationnode.data = "P" + random.choice(function_set)
            else:
                mutationnode.data = str(random.uniform(0, 1))
            new_a.nodes.clear()
            updateNodes(new_a, new_a.root)
            fit_a = a.fitness
            # print("current tree")
            # printTree(a.root)
            # print("mutated tree")
            # printTree(new_a.root)
            fit_new_a = calcFitness(new_a, sample, index)

            if fit_a >= fit_new_a:
                new_a = Tree()
                new_a.root = CloneTree(a.root)
                updateNodes(new_a, new_a.root)
                nodes = new_a.nodes.copy()
                for i in nodes:
                    if i.data in function_set:
                        funcnodes.append(i)
                    elif i.data not in function_set and i.data != "P" and i.data != "W" and i.data not in feature_set:
                        # print(i.data)
                        doublenodes.append(i)
                    elif i.data.startswith("P"):
                        pnodes.append(i)

                randomNum = random.uniform(0, 10)
                if len(funcnodes) == 0:
                    if randomNum < 7.283:
                        mutationnode = random.choice(pnodes)
                    else:
                        mutationnode = random.choice(doublenodes)
                else:
                    if randomNum < 3.2839:
                        mutationnode = random.choice(funcnodes)
                    elif 3.2839 < randomNum < 8.468:
                        mutationnode = random.choice(pnodes)
                    else:
                        mutationnode = random.choice(doublenodes)
            else:
                break
        else:
            new_a.root = CloneTree(a.root)
            updateNodes(new_a, new_a.root)
            calcFitness(new_a, sample, index)
            break
        cycle += 1
    return new_a


def sortPopulation(alist):
    if len(alist) > 1:
        mid = len(alist)//2
        lefthalf = alist[:mid]
        righthalf = alist[mid:]

        sortPopulation(lefthalf)
        sortPopulation(righthalf)
        i = 0
        j = 0
        k = 0
        while i < len(lefthalf) and j < len(righthalf):
            if lefthalf[i].cumulativefitness < righthalf[j].cumulativefitness:
                alist[k] = lefthalf[i]
                i = i+1
            else:
                alist[k] = righthalf[j]
                j = j+1
            k = k+1

        while i < len(lefthalf):
            alist[k] = lefthalf[i]
            i = i+1
            k = k+1

        while j < len(righthalf):
            alist[k] = righthalf[j]
            j = j+1
            k = k+1


# features = ["f0", "f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9"]
# data = pd.read_csv("kritika.csv")
# data = np.array(data)
# a = Node()
# t1 = Tree()
# b = Node()
# t2 = Tree()
# makeTree(t1, a, 6, features)
# makeTree(t2, b, 6, features)
# printTree(t1.root)
# printTree(t2.root)
# swapSubTrees(a.left, b.right)
# printTree(t1.root)
# printTree(t2.root)


# print(calcFitness(t1, data, 0))
# print(calcFitness(t2, data, 0))
# x, y = crossover(t1, t2, data, 0)
# printTree(x.root)
# printTree(y.root)
# print(calcFitness(x, data, 0))
# print(calcFitness(y, data, 0))
# root_loc=t1.nodes[0]
# ann = gptoanntree(t1.root)
# printTree(t1.root)
# printTree(ann)
# expr = []

# evalTree(t1, t1.root, data)
# dataset = pd.read_csv("EEGDataset.csv")
# training_data, testing_data = train_test_split(dataset, test_size=0.2)
# training_data = np.array(training_data)
# testing_data = np.array(testing_data)
# count = 0
# for data in training_data:
#     tree = Tree()
#     temp = CloneTree(t1.root)
#     tree.root = temp
#     evalTree(tree, temp, data)
#     printTree(tree)
#     count += float(tree.root.data)
# average = count/len(training_data)
# print(average)
# printTree(t1)
# calcFitness(t1,dataset)
# print(t1.fitness)
# printTree(t1)
# print(activationFunction(50))
# print(generateExpression(t1.root, expr))
# printTree(t2)

# ----------------------------------------Classifier Begins-------------------------------------------------------------
# ----------------------------------------Training Phase----------------------------------------------------------------

maxPopulation = 100
# maxFitnessCalcs = 40000
# maxGenerations = 5

trainingAcc = 90
print("Training accuracy = ", trainingAcc)
print("Population size = ", maxPopulation)
maxLevel = 6
noClasses = 8
dataset = pd.read_csv("Master.csv")
dataset = dataset.sample(frac=1)
norm_dataset = pd.DataFrame(preprocessing.normalize(dataset.iloc[:, 0:-1])).join(dataset.iloc[:, -1])
# print(norm_dataset)
# print(dataset)
# initial = dataset.iloc[:, 0:2]
# end = dataset.iloc[:, 2:-1].apply(np.log10).join(dataset.iloc[:, -1])
# dataset = initial.join(end)
training_data, testing_data = train_test_split(dataset, test_size=0)
training_data = np.array(training_data)
# testing_data = np.array(testing_data)
features = ["f0", "f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9"]

# ----------------------------------------Generate Population-----------------------------------------------------------
#
print("Classifier for Emotion Analysis through Neuro-Pyschological Data")
print("Made by combined efforts with Mentors Dr. Arpit Bhardwaj and Mrs. Divya Acharya")
initialPopulation = []
currentGeneration = []
all = []
while 1:

    print("\n")
    print("Options available:")
    print("1. Begin Population Generation")
    print("2. Train Classifier")
    print("3. Test Classifier")
    print("4. Exit")
    a = int(input("\nEnter your choice: "))
    if a == 1:
        print("Generating Initial Population...")
        li=[]
        for i in range(maxPopulation):
            temp = Individual()
            li.clear()
            if temp not in all:
                all.append(temp)
            # print("start = ", temp.trees)
            count1 = 0
            while 1:
                t = Tree()
                a = Node()
                makeTree(t, a, maxLevel, features)
                # print(t not in all)
                # print(t)
                if t not in all:
                    if count1 >= noClasses:
                        break
                    li.append(t)
                    all.append(t)
                    count1 += 1
                #     print(count1)
                # print(temp.trees)
                # print(all)
            temp.trees = li.copy()
            initialPopulation.append(temp)
            # print(temp.trees)
        print("---------------------------------------------------------------------------------------------------------")
        print("Generation 1 created\n")

        continue
    elif a == 2:
        currentGeneration = initialPopulation.copy()
        nextGeneration = []
        count = 0
        gen = 1
        while 1:
            max_fitness = []
            print("Calculating fitness of current generation...")
            # print(currentGeneration)
            for i in currentGeneration:
                i.cumulativefitness = 0
                for j in i.trees:
                    for k in range(0, 8):
                        # print(i.trees.index(j) == k)
                        if i.trees.index(j) == k:
                            # if j.fitness is None:
                                # temp = CloneTree(j.root)
                            tree = Tree()
                            tree.root = CloneTree(j.root)
                            fit = calcFitness(tree, training_data, k)
                            # print(fit)
                            count += 1
                            # print(j.fitness)
                            j.fitness = fit
                            # print(j.fitness)
                            # print(fit)
                            i.cumulativefitness += fit/8
                            # print("tree ", j, "fitness = ", fit/8)
                    # printTree(j.root)
                max_fitness.append(i.cumulativefitness)
                # print(i, "  ", i.cumulativefitness)
            print("\nMaximum fitness of current generation is ", max(max_fitness))
            print("\nSorting current generation individuals on the basis of fitness")
            sortPopulation(currentGeneration)
            # for i in currentGeneration[int(0.7*maxPopulation):maxPopulation]:
            #     print(i, "  ", i.cumulativefitness)
            # print(len(currentGeneration))
            if max(max_fitness) < trainingAcc:
                print("-------------------------------------------------------------------------------------------------")
                print("\nGenerating generation ", gen+1)
                print("\nExecuting mutation on first 10% individuals")
                for i in currentGeneration[0:int(0.1*maxPopulation)]:
                    # print(i)
                    for j in i.trees:
                        # print("current tree")
                        # printTree(j.root)
                        temp = mutation(j, training_data, i.trees.index(j))
                        # print("mutated tree")
                        # printTree(temp.root)
                        i.trees[i.trees.index(j)-1] = temp
                        count += 1
                    nextGeneration.append(i)
                # print(len(nextGeneration))
                print("Mutation complete")

                print("\nExecuting standard crossover on next 40% individuals")
                scrossed = currentGeneration[int(0.1 * maxPopulation):int(0.5 * maxPopulation)]
                for i in range(int(0.2*maxPopulation)):
                    parent1 = random.choice(scrossed)
                    scrossed.remove(parent1)
                    parent2 = random.choice(scrossed)
                    scrossed.remove(parent2)
                    for j in range(len(parent1.trees)):
                        a = parent1.trees[j]
                        b = parent2.trees[j]
                        n1, n2 = standardCrossover(a, b, j)
                        parent1.trees[parent1.trees.index(parent1.trees[j])] = n1
                        parent2.trees[parent2.trees.index(parent2.trees[j])] = n2
                    nextGeneration.append(parent1)
                    nextGeneration.append(parent2)
                # print(len(nextGeneration))
                print("Standard crossover complete")
                print("\nExecuting hill-climbing crossover on next 40% individuals")
                crossed = currentGeneration[int(0.5 * maxPopulation):int(0.9 * maxPopulation)]
                for i in range(int(0.2 * maxPopulation)):
                    parent1 = random.choice(crossed)
                    # print(parent1)
                    crossed.remove(parent1)
                    parent2 = random.choice(crossed)
                    crossed.remove(parent2)
                    for j in range(len(parent1.trees)):
                        a = parent1.trees[j]
                        b = parent2.trees[j]
                        n1, n2 = crossover(a, b, training_data, j)
                        count += 2
                        parent1.trees[parent1.trees.index(parent1.trees[j])] = n1
                        parent2.trees[parent2.trees.index(parent2.trees[j])] = n2
                    nextGeneration.append(parent1)
                    nextGeneration.append(parent2)
                # print(len(nextGeneration))
                print("Hill-climb crossover complete")
                print("\nReproducing remaining 10% individuals")
                for i in currentGeneration[int(0.9*maxPopulation):maxPopulation]:
                    nextGeneration.append(i)
                # print(len(nextGeneration))
                print("Reproduction complete")
            else:
                for i in currentGeneration:
                    nextGeneration.append(i)
                break
            for i in currentGeneration:
                currentGeneration.remove(i)
            currentGeneration.clear()
            # print("c1 = ", currentGeneration)
            # print("n1 = ", nextGeneration)
            # print("len = ", len(nextGeneration))
            # for j in nextGeneration:
            #     currentGeneration.append(j)
            currentGeneration = nextGeneration.copy()
            # print("c2 = ", currentGeneration)
            # print("len = ", len(currentGeneration))
            # for k in nextGeneration:
            #     nextGeneration.remove(k)
            nextGeneration.clear()
            # print("nf = ", nextGeneration)
            print("-----------------------------------------------------------------------------------------------------")
            print("\nGeneration ", gen+1, " created.")
            gen += 1
            continue
        with open("bestclassifier(87.5).pkl", "wb") as out:
            dill.dump(currentGeneration[-1], out)
    elif a == 3:
        testing_data = pd.read_csv("kritika.csv")
        # testing_data = pd.DataFrame(preprocessing.normalize(testing_data.iloc[:, 0:-1])).join(testing_data.iloc[:, -1])
        testing_data = np.array(testing_data)
        with open("bestclassifier(87.5).pkl", "rb") as inp:
            individual = dill.load(inp)
        out = None
        accFear0 = 0
        accTenderness1 = 0
        accAmusement2 = 0
        accJoy3 = 0
        accSadness4 = 0
        accDisgust5 = 0
        accAnger6 = 0
        accNeutral7 = 0
        res = None
        tp = 0
        tn = 0
        fp = 0
        fn = 0
        print("Started Testing on available test data...")

        for k in testing_data:
            for j in individual.trees:
                temp = CloneTree(j.root)
                tree = Tree()
                tree.root = temp
                evalTree(tree, temp, k)
                out = float(tree.root.data)
                # print(out)
                if out > 0:
                    if individual.trees.index(j) == 0:
                        res = 0
                    elif individual.trees.index(j) == 1:
                        res = 1
                    elif individual.trees.index(j) == 2:
                        res = 2
                    elif individual.trees.index(j) == 3:
                        res = 3
                    elif individual.trees.index(j) == 4:
                        res = 4
                    elif individual.trees.index(j) == 5:
                        res = 5
                    elif individual.trees.index(j) == 6:
                        res = 6
                    elif individual.trees.index(j) == 7:
                        res = 7

                else:
                    if res is None and k[-1] != 0 and individual.trees.index(j) == 0:
                        accFear0 += 1
                        tn += 1
                        # print("Fear = ", accFear0)
                    elif res is None and k[-1] != 1 and individual.trees.index(j) == 1:
                        accTenderness1 += 1
                        tn += 1
                        # print("Tenderness = ", accTenderness1)
                    elif res is None and k[-1] != 2 and individual.trees.index(j) == 2:
                        accAmusement2 += 1
                        tn += 1
                        # print("Amusement = ", accAmusement2)
                    elif res is None and k[-1] != 3 and individual.trees.index(j) == 3:
                        accJoy3 += 1
                        tn += 1
                        # print("joy = ", accJoy3)
                    elif res is None and k[-1] != 4 and individual.trees.index(j) == 4:
                        accSadness4 += 1
                        tn += 1
                        # print("sadness = ", accSadness4)
                    elif res is None and k[-1] != 5 and individual.trees.index(j) == 5:
                        accDisgust5 += 1
                        tn += 1
                        # print("disgust = ", accDisgust5)
                    elif res is None and k[-1] != 6 and individual.trees.index(j) == 6:
                        accAnger6 += 1
                        tn += 1
                        # print("anger = ", accAnger6)
                    elif res is None and k[-1] != 7 and individual.trees.index(j) == 7:
                        accNeutral7 += 1
                        tn += 1
                        # print("neutral = ", accNeutral7)
                    elif res is None and k[-1] == 0 and individual.trees.index(j) == 0:
                        fn += 1
                    elif res is None and k[-1] == 1 and individual.trees.index(j) == 1:
                        fn += 1
                    elif res is None and k[-1] == 2 and individual.trees.index(j) == 2:
                        fn += 1
                    elif res is None and k[-1] == 3 and individual.trees.index(j) == 3:
                        fn += 1
                    elif res is None and k[-1] == 4 and individual.trees.index(j) == 4:
                        fn += 1
                    elif res is None and k[-1] == 5 and individual.trees.index(j) == 5:
                        fn += 1
                    elif res is None and k[-1] == 6 and individual.trees.index(j) == 6:
                        fn += 1
                    elif res is None and k[-1] == 7 and individual.trees.index(j) == 7:
                        fn += 1
                # print(res, k[-1])
                if res == 0 and k[-1] == 0:
                    tp += 1
                    accFear0 += 1

                    # print("Fear = ", accFear0)
                elif res == 1 and k[-1] == 1:
                    accTenderness1 += 1
                    tp += 1
                    # print("Tenderness = ", accTenderness1)
                elif res == 2 and k[-1] == 2:
                    accAmusement2 += 1
                    tp += 1
                    # print("Amusement = ", accAmusement2)
                elif res == 3 and k[-1] == 3:
                    accJoy3 += 1
                    tp += 1
                    # print("joy = ", accJoy3)
                elif res == 4 and k[-1] == 4:
                    accSadness4 += 1
                    tp += 1
                    # print("sadness = ", accSadness4)
                elif res == 5 and k[-1] == 5:
                    accDisgust5 += 1
                    tp += 1
                    # print("disgust = ", accDisgust5)
                elif res == 6 and k[-1] == 6:
                    accAnger6 += 1
                    tp += 1
                    # print("anger = ", accAnger6)
                elif res == 7 and k[-1] == 7:
                    accNeutral7 += 1
                    tp += 1
                    # print("neutral = ", accNeutral7)
                elif res == 0 and k[-1] != 0:
                    fp += 1
                elif res == 1 and k[-1] != 1:
                    fp += 1
                elif res == 2 and k[-1] != 2:
                    fp += 1
                elif res == 3 and k[-1] != 3:
                    fp += 1
                elif res == 4 and k[-1] != 4:
                    fp += 1
                elif res == 5 and k[-1] != 5:
                    fp += 1
                elif res == 6 and k[-1] != 6:
                    fp += 1
                elif res == 7 and k[-1] != 7:
                    fp += 1

        # accFear0 = accFear0 / (len(pd.DataFrame(testing_data).loc[(pd.DataFrame(testing_data).iloc[:, -1] == 0)]))*100
        # accTenderness1 = accTenderness1 / (len(pd.DataFrame(testing_data).loc[(pd.DataFrame(testing_data).iloc[:, -1] == 1)]))*100
        # accAmusement2 = accAmusement2 / (len(pd.DataFrame(testing_data).loc[(pd.DataFrame(testing_data).iloc[:, -1] == 2)]))*100
        # accJoy3 = accJoy3 / (len(pd.DataFrame(testing_data).loc[(pd.DataFrame(testing_data).iloc[:, -1] == 3)]))*100
        # accSadness4 = accSadness4 / (len(pd.DataFrame(testing_data).loc[(pd.DataFrame(testing_data).iloc[:, -1] == 4)]))*100
        # accDisgust5 = accDisgust5 / (len(pd.DataFrame(testing_data).loc[(pd.DataFrame(testing_data).iloc[:, -1] == 5)]))*100
        # accAnger6 = accAnger6 / (len(pd.DataFrame(testing_data).loc[(pd.DataFrame(testing_data).iloc[:, -1] == 6)]))*100
        # accNeutral7 = accNeutral7 / (len(pd.DataFrame(testing_data).loc[(pd.DataFrame(testing_data).iloc[:, -1] == 7)]))*100
        # print(len(pd.DataFrame(testing_data).loc[(pd.DataFrame(testing_data).iloc[:, -1] == 0)]))
        # print(len(pd.DataFrame(testing_data).loc[(pd.DataFrame(testing_data).iloc[:, -1] == 1)]))
        # print(len(pd.DataFrame(testing_data).loc[(pd.DataFrame(testing_data).iloc[:, -1] == 2)]))
        # print(len(pd.DataFrame(testing_data).loc[(pd.DataFrame(testing_data).iloc[:, -1] == 3)]))
        # print(len(pd.DataFrame(testing_data).loc[(pd.DataFrame(testing_data).iloc[:, -1] == 4)]))
        # print(len(pd.DataFrame(testing_data).loc[(pd.DataFrame(testing_data).iloc[:, -1] == 5)]))
        # print(len(pd.DataFrame(testing_data).loc[(pd.DataFrame(testing_data).iloc[:, -1] == 6)]))
        # print(len(pd.DataFrame(testing_data).loc[(pd.DataFrame(testing_data).iloc[:, -1] == 7)]))
        # print("neutral", accNeutral7)

        # print("Testing completed on test data.")
        # print("Accuracy for Class 0 or Fear is ", accFear0, "%")
        # print("Accuracy for Class 1 or Tenderness is ", accTenderness1, "%")
        # print("Accuracy for Class 2 or Amusement is ", accAmusement2, "%")
        # print("Accuracy for Class 3 or Joy is ", accJoy3, "%")
        # print("Accuracy for Class 4 or Sadness is ", accSadness4, "%")
        # print("Accuracy for Class 5 or Disgust is ", accDisgust5, "%")
        # print("Accuracy for Class 6 or Anger is ", accAnger6, "%")

        accFear0 = (accFear0 / (len(testing_data)))*100
        accTenderness1 = (accTenderness1 / (len(testing_data)))*100
        accAmusement2 = (accAmusement2 / (len(testing_data)))*100
        accJoy3 = (accJoy3 / (len(testing_data)))*100
        accSadness4 = (accSadness4 / (len(testing_data)))*100
        accDisgust5 = (accDisgust5 / (len(testing_data)))*100
        accAnger6 = (accAnger6 / (len(testing_data)))*100
        accNeutral7 = (accNeutral7/len(testing_data))*100

        print("Testing completed on test data.")
        print("Accuracy for Class 0 or Fear is ", accFear0, "%")
        print("Accuracy for Class 1 or Tenderness is ", accTenderness1, "%")
        print("Accuracy for Class 2 or Amusement is ", accAmusement2, "%")
        print("Accuracy for Class 3 or Joy is ", accJoy3, "%")
        print("Accuracy for Class 4 or Sadness is ", accSadness4, "%")
        print("Accuracy for Class 5 or Disgust is ", accDisgust5, "%")
        print("Accuracy for Class 6 or Anger is ", accAnger6, "%")
        print("Accuracy for Class 7 or Neutral is ", accNeutral7, "%")
        # print("\n \n")
        avgaccuracy = (accFear0+accTenderness1+accAmusement2+accJoy3+accSadness4+accDisgust5+accAnger6+accNeutral7)/8
        print("Overall average accuracy of classifier is ", avgaccuracy, "%")
        # print("\n")
        # print("True Positive = \n", tp)
        # print("True Negative = \n", tn)
        # print("False Positive = \n", fp)
        # print("False Negative = \n", fn)
        # p = tp/(tp+fp)
        # r = tp/(tp+fn)
        # F1Score = 2*p*r/(p+r)
        # print("F1-Score of classifier is ", F1Score)
        accuracypos = (accJoy3+accAmusement2+accTenderness1)/3
        # print("\n")
        print("Average accuracy for 3 positive emotions (Joy, Amusement, Tenderness) is ", accuracypos, "%")
        accuracyneg = (accAnger6+accDisgust5+accSadness4+accFear0)/4
        # print("\n")
        print("Average accuracy for 4 negative emotions (Fear, Sadness, Disgust, Anger) is ", accuracyneg, "%")
    elif a == 4:
        break
