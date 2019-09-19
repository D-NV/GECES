import pandas as pd
import random
import numpy as np


class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None


class Tree:
    def __init__(self):
        self.root = None


def populate(classes, maxheight, features, terminals):
    if classes == 2:
        population = []
        for i in range(100):
            t = Tree()
            t.root = Node(random.choice(terminals))
            population.append(t)
        for each in population:
            generateTree(1, maxheight, features, terminals, each.root)
    else:
        population = []
        for i in range(100):
            classifier = []
            for j in range(classes):
                t = Tree()
                t.root = Node(random.choice(terminals))
                classifier.append(t)
            population.append(classifier)
        for classifier in population:
            for each in classifier:
                generateTree(1, maxheight, features, terminals, each.root)
    return population


def generateTree(level, maxheight, features, terminals, curNode):
    if level < maxheight-1:
        if curNode.data in terminals:
            r = random.random()
            if r <= 0.5:
                r1 = random.random()
                if r1 < 0.95:
                    curNode.left = Node(random.choice(terminals))
                    generateTree(level+1, maxheight, features, terminals, curNode.left)
                else:
                    curNode.left = Node(random.randint(-10000, 10000))
                r2 = random.random()
                if r2 < 0.95:
                    curNode.right = Node(random.choice(terminals))
                    generateTree(level + 1, maxheight, features, terminals, curNode.right)
                else:
                    curNode.right = Node(random.randint(-10000, 10000))
            elif 0.5 < r <= 0.7:
                r1 = random.random()
                if r1 < 0.95:
                    curNode.left = Node(random.choice(terminals))
                    generateTree(level + 1, maxheight, features, terminals, curNode.left)
                else:
                    curNode.left = Node(random.randint(-10000, 10000))
                curNode.right = Node(random.choice(features))
            elif 0.7 < r <= 0.9:
                curNode.left = Node(random.choice(features))
                r2 = random.random()
                if r2 < 0.95:
                    curNode.right = Node(random.choice(terminals))
                    generateTree(level + 1, maxheight, features, terminals, curNode.right)
                else:
                    curNode.right = Node(random.randint(-10000, 10000))
            else:
                curNode.left = Node(random.choice(features))
                curNode.right = Node(random.choice(features))
    elif level == maxheight-1:
        if curNode.data in terminals:
            r = random.random()
            if r <= 0.3:
                curNode.left = Node(random.choice(features))
                curNode.right = Node(random.choice(features))
            elif 0.3 < r <= 0.6:
                curNode.left = Node(random.randint(-10000, 10000))
                curNode.right = Node(random.choice(features))
            elif 0.6 < r <= 0.9:
                curNode.left = Node(random.choice(features))
                curNode.right = Node(random.randint(-10000, 10000))
            else:
                curNode.left = Node(random.randint(-10000, 10000))
                curNode.right = Node(random.randint(-10000, 10000))


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


def postOrder(root, expr_post):
    if root is not None:
        postOrder(root.left, expr_post)
        postOrder(root.right, expr_post)
        expr_post.append(root.data)
    return expr_post


def find_terminals(tree, functions):
    root = tree.root
    expr_post = []
    expr_post = postOrder(root, expr_post)
    # print(expr_post)
    terminals, non_terminals = [], []
    for i in expr_post:
        # print(i)
        if i in functions:
            non_terminals.append(i)
        else:
            terminals.append(i)
    return terminals, non_terminals


def crossover_std(p1, p2, functions):
    terminals_p1, non_terminals_p1 = find_terminals(p1, functions)
    terminals_p2, non_terminals_p2 = find_terminals(p2, functions)
    

functions = ['+', '-', '*', '/']
features = ['f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10']
maxheight = 6
classes = 8
a = Tree()
a.root = Node(random.choice(functions))
generateTree(1, maxheight, features, functions, a.root)
printTree(a.root)
b = Tree()
b.root = Node(random.choice(functions))
generateTree(1, maxheight, features, functions, b.root)
printTree(b.root)
crossover_std(a, b, functions)
# population = populate(classes, maxheight, features, functions)
# print(np.array(population))

