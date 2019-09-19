import numpy as np
import pandas as pd
import tensorflow as tf
import random

class Classifier:
    def __init__(self, tree, fitness, cumulative_fitness):
        self.tree = tree
        self.fitness = fitness
        self.cumulative_fitness = cumulative_fitness

        self.tree = []
        self.fitness = []

    def classifier(self, classes):
        for i in range(classes):
            self.tree.append(Node())

    def __eq__(self, other):
        cf1 = self.cumulative_fitness
        cf2 = other.cumulative_fitness
        if cf1>cf2:
            return 1
        elif cf1<cf2:
            return -1
        else:
            return 0


class Junction:
    def __init__(self, data, left, left_cost, right, right_cost):
        self.data = data
        self.left = left
        self.right = right
        self.left_cost = left_cost
        self.right_cost = right_cost


class Node:
    def __init__(self, data='', left=None, right=None, parent=None):
        self.data = data
        self.left = left
        self.right = right
        self.parent = parent




class Tree:
    def __init__(self, root, fitness_value):
        self.root = root
        self.fitness_value = fitness_value

    def __eq__(self, other):
        f1 = self.fitness_value
        f2 = other.fitness_value
        if f1>f2:
            return 1
        elif f1<f2:
            return -1
        else:
            return 0

class CrossOverSort:
    def __init__(self, child, parent, fitness_value):
        self.child = child
        self.parent = parent
        self.fitness_value = fitness_value


class createTree:
    root = Node()
    expr_pre = ''
    expr_in = ''

    OPTION_ARTH_OPERATOR = 0
    OPTION_INPUT_SIGNAL = 1
    OPTION_DOUBLE_NUM = 2
    OPTION_W = 3
    OPTION_P = 4

    expr_post = []

    def CheckForSinCos(self, str):
        if str == 'sin' or str == 'cos':
            return True
        else:
            return False

    def makeTree(self, root, maxlevel, features):
        function_set = {'+', '-', '*', '/', '^'}
        try:
            root.data = random.choice(function_set)
            root.parent = None
            self.generateTree(root, 1, features, maxlevel)
        except:
            print('Error in makeTree() function')

    def generateTree(self, curNode, level, features, maxlevel):
        function_set = ['+', '-', '*', '/', '^', 'sin', 'cos']
        varSet = features
        for i in range(0, len(features)):
            varSet[i] = i

        if maxlevel == 0:
            return
        if self.CheckForSinCos(curNode.data):
            curNode.left = Node()
            curNode.left.parent = curNode
        else:
            curNode.left = Node()
            curNode.left.parent = curNode
            curNode.right = Node()
            curNode.right.parent = curNode

        if level < maxlevel:
            randomNum = random.uniform(0, 1)

            if randomNum < 0.55:
                curNode.left.data = random.choice(function_set)

                if curNode.right is not None:
                    curNode.right.data = random.choice(function_set)

                self.generateTree(curNode.left, level+1, features, maxlevel)

                if curNode.right is not None:
                    self.generateTree(curNode.right, level + 1, features, maxlevel)

            elif randomNum < 0.7 and randomNum > 0.56:
                curNode.left.data = random.choice(function_set)